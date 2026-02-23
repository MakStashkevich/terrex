import asyncio
import struct
import time
import traceback

from terrex import packet
from terrex.net import module
from terrex.net.enum.teleport_pylon_operation import TeleportPylonOperation
from terrex.net.enum.teleport_pylon_type import TeleportPylonType
from terrex.net.enum.teleport_request_type import TeleportRequestType
from terrex.net.enum.teleport_type import TeleportType
from terrex.net.structure.vec2 import Vec2
from terrex.packet.base import Packet, packet_registry
from terrex.net.creative_power.spawn_rate_slider_per_player_power import (
    SpawnRateSliderPerPlayerPower,
)
from terrex.net.module import NetCreativePowersModule
from terrex.id import MessageID
from terrex.net.enum.mode import NetMode
from terrex.localization.localization import get_translation
from terrex.net.streamer import Reader, Writer

PLAYER_UUID = "01032c81-623f-4435-85e5-e0ec816b09ca"


class Client:
    def __init__(
        self,
        host: str,
        port: int,
        protocol: int,
        server_password: str,
        terrex,
    ):
        from terrex.terrex import Terrex

        if not isinstance(terrex, Terrex):
            raise TypeError("terrex must be a Terrex instance")

        self.host = host
        self.port = port
        self.protocol = protocol
        self.server_password = server_password

        self.terrex = terrex
        self.player = terrex.player
        self.world = terrex.world
        self.evman = terrex.evman

        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.send_queue = asyncio.Queue()
        self.recv_queue = asyncio.Queue()
        self.running = False
        self.connected_to_server = False
        self.reader_task: asyncio.Task | None = None
        self.writer_task: asyncio.Task | None = None
        self.ping_task: asyncio.Task | None = None
        self.current_ping = 0
        self._waiting_ping = False
        self._ping_last_sent = 0.0
        self._ping_start_time = 0.0

        self.handle_queue = asyncio.Queue()
        self.handle_task: asyncio.Task | None = None

    async def connect(self) -> None:
        """Connect to the server and perform a handshake."""
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.running = True

        self.reader_task = asyncio.create_task(self._reader_loop())
        self.writer_task = asyncio.create_task(self._writer_loop())
        self.handle_task = asyncio.create_task(self._handle_loop())

        await asyncio.sleep(0.1)

        # Send connect packet
        await self.send(packet.Hello(self.protocol))

    async def send(self, packet: Packet, wait: bool = False) -> None:
        """
        Send packet to queue.

        If wait=True, wait until packet is actually written
        to the underlying stream (writer.drain()).
        """

        if not wait:
            await self.send_queue.put((packet, None))
            return

        sent_event = asyncio.Event()
        await self.send_queue.put((packet, sent_event))
        await sent_event.wait()

    async def recv(self) -> Packet | None:
        """Get a (blocking) package."""
        try:
            return await self.recv_queue.get()
        except asyncio.TimeoutError:
            return None

    async def try_recv(self) -> Packet | None:
        """Get a non-blocking package."""
        try:
            return await self.recv_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def _read_exact(self, n: int) -> bytes:
        """Read exactly n bytes."""
        data = b""
        while len(data) < n:
            chunk = await self.reader.read(n - len(data))
            if len(chunk) == 0:
                raise ConnectionError("The connection is closed")
            data += chunk
        return data

    async def _reader_loop(self) -> None:
        """The packet reading stream."""
        try:
            while self.running:
                try:
                    len_bytes = await self._read_exact(2)
                    length = struct.unpack("<H", len_bytes)[0]
                    payload_full = await self._read_exact(length - 2)
                    packet_id = payload_full[0]
                    payload = payload_full[1:]

                    packet_cls = packet_registry.get(packet_id)
                    if packet_cls:
                        packet = packet_cls()
                        reader = Reader(payload, protocol_version=self.protocol, net_mode=NetMode.SERVER)
                        packet.read(reader)

                        if not self.running:
                            continue

                        await self.handle_queue.put(packet)

                        if not await self._handle_server_packet(packet):
                            continue

                        await self.recv_queue.put(packet)
                    else:
                        try:
                            name = MessageID(packet_id).name
                        except ValueError:
                            name = "UNKNOWN"
                        print(f"Unknown ID packet: 0x{packet_id:02X}, name: {name}")
                        continue
                except asyncio.TimeoutError:
                    continue
                except ConnectionError:
                    break
                except Exception as e:
                    print(traceback.format_exc())
                    print(f"Error read packet by client: {e}")
                    break
        except asyncio.CancelledError:
            self.running = False

    async def _handle_server_packet(self, pkt: Packet) -> bool:
        if not self.running:
            return False

        if pkt.id == MessageID.Ping:
            await self.on_ping_received()
            return False

        if pkt.id == MessageID.Kick and isinstance(pkt, packet.Kick):
            print(f"Disconnect with reason: {get_translation(packet.reason)}")
            await self.stop()
            return False

        if not self.connected_to_server:
            # server req password
            if pkt.id == MessageID.RequestPassword:
                pkt = packet.SendPassword(self.server_password)
                await self.send(pkt)

            # server accept password and receive player info
            if pkt.id == MessageID.PlayerInfo and isinstance(pkt, packet.PlayerInfo) and not pkt.is_server:
                # save server player id
                self.world.my_player_id = self.player.id = pkt.player_id
                self.world.players[pkt.player_id] = self.player

                # send player info to server
                player_info = packet.SyncPlayer(
                    player_id=self.player.id,
                    skin_variant=self.player.skin_variant,
                    voice_variant=self.player.voice_variant,
                    voice_pitch_offset=self.player.voice_pitch_offset,
                    hair=self.player.hair,
                    name=self.player.name,
                    hair_dye=self.player.hair_dye,
                    accessory_visibility=self.player.accessory_visibility,
                    hide_misc=self.player.hide_misc,
                    hair_color=self.player.hair_color,
                    skin_color=self.player.skin_color,
                    eye_color=self.player.eye_color,
                    shirt_color=self.player.shirt_color,
                    under_shirt_color=self.player.under_shirt_color,
                    pants_color=self.player.pants_color,
                    shoe_color=self.player.shoe_color,
                )
                player_info.set_difficulty(self.player.difficulty)
                # player_info.set_hide_visible_accessory(self.player.accessory_visibility)
                # biome_torch_flags
                player_info.using_biome_torches = self.player.using_biome_torches
                player_info.happy_fun_torch_time = self.player.happy_fun_torch_time
                player_info.unlocked_biome_torches = self.player.unlocked_biome_torches
                player_info.unlocked_super_cart = self.player.unlocked_super_cart
                player_info.enabled_super_cart = self.player.enabled_super_cart
                # consumables_flags
                player_info.used_aegis_crystal = self.player.used_aegis_crystal
                player_info.used_aegis_fruit = self.player.used_aegis_fruit
                player_info.used_arcane_crystal = self.player.used_arcane_crystal
                player_info.used_galaxy_pearl = self.player.used_galaxy_pearl
                player_info.used_gummy_worm = self.player.used_gummy_worm
                player_info.used_ambrosia = self.player.used_ambrosia
                player_info.ate_artisan_bread = self.player.ate_artisan_bread
                await self.send(player_info)

                await self.send(packet.ClientUUID(PLAYER_UUID))
                await self.send(
                    packet.PlayerLifeMana(
                        player_id=self.player.id,
                        hp=self.player.currHP,
                        max_hp=self.player.maxHP,
                    )
                )
                await self.send(
                    packet.PlayerMana(
                        player_id=self.player.id,
                        mana=self.player.currMana,
                        max_mana=self.player.maxMana,
                    )
                )
                await self.send(packet.PlayerBuffs(player_id=self.player.id, buffs=[0] * 22))
                await self.send(
                    packet.SyncLoadout(
                        player_id=self.player.id,
                        loadout_index=0,
                        accessory_visibility=self.player.accessory_visibility,
                    )
                )
                for i in range(0, 139):  # 138
                    await self.send(
                        packet.SyncEquipment(
                            player_id=self.player.id,
                            slot_id=i,
                            stack=0,
                            prefix=0,
                            item_netid=0,
                        )
                    )
                for i in range(299, 339):  # 338
                    await self.send(
                        packet.SyncEquipment(
                            player_id=self.player.id,
                            slot_id=i,
                            stack=0,
                            prefix=0,
                            item_netid=0,
                        )
                    )
                for i in range(499, 540):  # 539
                    await self.send(
                        packet.SyncEquipment(
                            player_id=self.player.id,
                            slot_id=i,
                            stack=0,
                            prefix=0,
                            item_netid=0,
                        )
                    )
                for i in range(700, 740):  # 739
                    await self.send(
                        packet.SyncEquipment(
                            player_id=self.player.id,
                            slot_id=i,
                            stack=0,
                            prefix=0,
                            item_netid=0,
                        )
                    )
                for i in range(900, 990):  # 989
                    await self.send(
                        packet.SyncEquipment(
                            player_id=self.player.id,
                            slot_id=i,
                            stack=0,
                            prefix=0,
                            item_netid=0,
                        )
                    )
                await self.send(packet.RequestWorldData())
                # server: WORLD_INFO
                await self.send(packet.SpawnTileData(spawn_x=-1, spawn_y=-1))
                # server: WORLD_INFO & STATUS (load data by blocks...) & SEND_SECTION's, Unknown(0x9B) {'id': 155, 'raw': '1b012800'}, UPDATE_CHEST_ITEM's
                self.player.initialized = True

            # server say: you can spawn player
            if pkt.id == MessageID.InitialSpawn:
                await self.send(
                    packet.PlayerSpawn(
                        player_id=self.player.id,
                        spawn_x=-1,
                        spawn_y=-1,
                        respawn_time_remaining=0,
                        number_of_deaths_pve=0,
                        number_of_deaths_pvp=0,
                        team_id=2,  # todo: move to player
                        player_spawn_context=1,
                    )
                )
                await self.send(
                    packet.NetModules(
                        module=NetCreativePowersModule.create(power=SpawnRateSliderPerPlayerPower.create(value=0.0)),
                    )
                )
                self.player.logged_in = True
                # then server send: NPC_HOME_UPDATE (0-29), current ANGLER_QUEST, 6 packets of SYNC_REVENGE_MARKER

            # server say: you successful connected to server
            if pkt.id == MessageID.FinishedConnectingToServer:
                # then server send: NetModules (with messages MOTD & connect success player)
                # UPDATE_TILE_ENTITY
                self.connected_to_server = True

                if self.ping_task is None:
                    self.ping_task = asyncio.create_task(self._ping_loop())

                # Set player teem if needed
                await self.send(
                    packet.TeamChange(
                        player_id=self.player.id,
                        team=2,  # todo: green team, move to player
                    )
                )

                # -------- repeated every minute --------
                await self.send(
                    packet.SyncPlayerZone(
                        player_id=self.player.id,
                        # todo: add all zone flags
                    )
                )
                await self.send(packet.PlayerBuffs(player_id=self.player.id, buffs=[0] * 22))  # repeat???

                # ---0x0D UPDATE_PLAYER (0x0D) ---
                # {'player_id': 0, 'keys': 64, 'pulley': 16, 'action': 10, 'sleep_info': 0, 'selected_item': 0, 'pos': {'x': 67166.0, 'y': 6742.0, 'TILE_TO_POS_SCALE': 16.0}, 'vel': None, 'original_and_home_pos': None}

                # ---0x0D UPDATE_PLAYER (0x0D) ---
                # {'player_id': 0, 'keys': 64, 'pulley': 16, 'action': 10, 'sleep_info': 2, 'selected_item': 0, 'pos': {'x': 67166.0, 'y': 6742.0, 'TILE_TO_POS_SCALE': 16.0}, 'vel': None, 'original_and_home_pos': None}

                # --------- end repeated block

                await self.send(
                    packet.UpdatePlayerLuckFactors(
                        player_id=self.player.id,
                        ladybug_luck_time_left=self.player.ladybug_luck_time_left,
                        torch_luck=self.player.torch_luck,
                        luck_potion=self.player.luck_potion,
                        has_garden_gnome_nearby=self.player.has_garden_gnome_nearby,
                        broken_mirror_bad_luck=self.player.broken_mirror_bad_luck,
                        equipment_based_luck_bonus=self.player.equipment_based_luck_bonus,
                        coin_luck=self.player.coin_luck,
                        kite_luck_level=self.player.kite_luck_level,
                    )
                )
                # Update npc names from 0 to 29
                for i in range(29):
                    await self.send(packet.UniqueTownNPCInfoSyncRequest(npc_id=i, name=None, town_npc_variation_idx=None))

        if pkt.id == MessageID.TeleportEntity and isinstance(pkt, packet.TeleportEntity) and pkt.flags.need_sync:
            # updating player position and notifying the server about the successful teleportation
            self.player.position = pkt.position
            await self.send(
                packet.TeleportEntity(
                    server_synced=True,
                    player_teleport=True,
                    player_id=pkt.player_id,
                    position=Vec2(0, 0),
                    type=TeleportType.TeleporterTile,
                    pylon_type=TeleportPylonType.SurfacePurity,
                )
            )

        return True

    async def _writer_loop(self) -> None:
        """
        Internal writer loop.
        Pulls packets from queue and writes them to the socket.
        """
        try:
            while self.running:
                try:
                    item = await self.send_queue.get()
                    if item is None:
                        break
                    packet, sent_event = item
                    if not self.running:
                        continue
                    if not isinstance(packet, Packet):
                        continue
                    writer = Writer(protocol_version=self.protocol, net_mode=NetMode.CLIENT)
                    writer.write_byte(packet.id)
                    packet.write(writer)
                    payload = writer.bytes()
                    len_bytes = struct.pack("<H", len(payload) + 2)
                    full_packet = len_bytes + payload
                    self.writer.write(full_packet)
                    await self.writer.drain()
                    if sent_event and isinstance(sent_event, asyncio.Event):
                        sent_event.set()
                except asyncio.TimeoutError:
                    continue
                except ConnectionError:
                    break
                except Exception as e:
                    print(traceback.format_exc())
                    print(f"Error send packet by client: {e}")
                    break
        except asyncio.CancelledError:
            self.running = False

    async def send_ping(self) -> None:
        """Send a ping packet."""
        await self.send(packet.Ping())

    async def on_ping_received(self) -> None:
        """Process the received ping."""
        now = time.time() * 1000
        self.current_ping = int(now - self._ping_start_time)
        self._waiting_ping = False

    async def update_ping(self) -> None:
        """Update the ping logic."""
        now = time.time() * 1000
        if self._waiting_ping:
            self.current_ping = max(self.current_ping, int(now - self._ping_start_time))
            return
        if now - self._ping_last_sent >= 250:
            self._ping_start_time = now
            self._waiting_ping = True
            await self.send_ping()
            self._ping_last_sent = now

    async def _ping_loop(self) -> None:
        """Ping stream."""
        try:
            while self.running:
                await self.update_ping()
                await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            self.reset_ping()
            self.running = False

    async def _handle_loop(self) -> None:
        """Handle event-handles packets in a separate thread."""
        try:
            while self.running:
                try:
                    packet: Packet | None = await self.handle_queue.get()
                    if packet is None:
                        break
                    if not self.running:
                        continue
                    if not isinstance(packet, Packet):
                        continue
                    try:
                        await packet.handle(self.world, self.player, self.evman)
                    except NotImplementedError:
                        pass
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(traceback.format_exc())
                    print(f"Error handle packet: {e}")
                    break
        except asyncio.CancelledError:
            self.running = False

    def reset_ping(self) -> None:
        """Reset the ping."""
        self.current_ping = 0
        self._waiting_ping = False
        self._ping_last_sent = 0.0
        self._ping_start_time = 0.0

    async def stop(self) -> None:
        """Gracefully stop the client."""
        if not self.running:
            return
        self.running = False

        # Stop event manager, dispatcher with threads
        self.evman.stop()

        # Signal queues to stop
        try:
            await self.send_queue.put(None)
        except Exception:
            pass

        try:
            await self.handle_queue.put(None)
        except Exception:
            pass

        # Close writer
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass

        # Cancel tasks safely
        tasks = [self.reader_task, self.writer_task, self.handle_task, self.ping_task]
        for t in tasks:
            if t and not t.done():
                t.cancel()

    async def _request_teleport(self, type: TeleportRequestType) -> None:
        await self.send(packet.RequestTeleportationByServer(type=type))

    async def _teleport_entity(self, position: Vec2, type: TeleportType, player_teleport: bool = True) -> None:
        await self.send(
            packet.TeleportEntity(
                server_synced=False,
                player_teleport=player_teleport,
                player_id=self.player.id,
                position=position,
                type=type,
            )
        )

    async def _request_teleport_pylon(self, x: int, y: int, type: TeleportPylonType) -> None:
        await self.send(packet.NetModules(module=module.NetTeleportPylonModule.create(operation=TeleportPylonOperation.HandleTeleportRequest, x=x, y=y, pylon_type=type)))
