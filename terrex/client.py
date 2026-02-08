import socket
import struct
import threading
import queue
import time
from typing import Optional

from terrex import packets, structures
from terrex.packets.base import registry, Packet
from terrex.data.world import World
from terrex.data.player import Player
from terrex.events.eventmanager import EventManager
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer
from terrex.util.localization import get_translation

PLAYER_UUID = "01032c81-623f-4435-85e5-e0ec816b09ca"


class Client:
    def __init__(
        self,
        host: str,
        port: int,
        protocol: int,
        server_password: str,
        player: Player,
        world: World,
        evman: EventManager,
    ):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.server_password = server_password
        self.player = player
        self.world = world
        self._evman = evman

        self.sock: Optional[socket.socket] = None
        self.send_queue = queue.Queue()
        self.recv_queue = queue.Queue()
        self.running = False
        self.connected_to_server = False
        self.reader_thread: Optional[threading.Thread] = None
        self.writer_thread: Optional[threading.Thread] = None
        self.ping_thread: Optional[threading.Thread] = None
        self.current_ping = 0
        self._waiting_ping = False
        self._ping_last_sent = 0.0
        self._ping_start_time = 0.0

    def connect(self) -> None:
        """Подключиться к серверу и выполнить handshake."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.running = True

        self.reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self.writer_thread = threading.Thread(target=self._writer_loop, daemon=True)
        self.reader_thread.start()
        self.writer_thread.start()

        time.sleep(0.1)  # Дать потокам запуститься

        # Send connect packet
        self.send(packets.Connect(self.protocol))

    def send(self, packet: Packet) -> None:
        """Отправить пакет в очередь."""
        self.send_queue.put(packet)

    def recv(self) -> Optional[Packet]:
        """Получить пакет (блокирующий)."""
        try:
            return self.recv_queue.get(timeout=0.1)
        except queue.Empty:
            return None

    def try_recv(self) -> Optional[Packet]:
        """Получить пакет неблокирующий."""
        try:
            return self.recv_queue.get_nowait()
        except queue.Empty:
            return None

    def _recv_exact(self, n: int) -> bytes:
        """Прочитать точно n байт."""
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if len(chunk) == 0:
                raise ConnectionError("Соединение закрыто")
            data += chunk
        return data

    def _reader_loop(self) -> None:
        """Поток чтения пакетов."""
        while self.running:
            try:
                len_bytes = self._recv_exact(2)
                length = struct.unpack("<H", len_bytes)[0]
                payload_full = self._recv_exact(length - 2)
                packet_id = payload_full[0]
                payload = payload_full[1:]

                # print(f"[READ] ID пакета: 0x{packet_id:02X}")
                packet_cls = registry.get(packet_id)
                if packet_cls:
                    packet = packet_cls()
                    reader = Reader(payload)
                    packet.read(reader)
                    packet.handle(self.world, self.player, self._evman)

                    if not self._handle_server_packet(packet):
                        continue

                    self.recv_queue.put(packet)
                else:
                    print(
                        f"Неизвестный ID пакета: 0x{packet_id:02X}, name: {PacketIds[packet_id].name}"
                    )
            except (ConnectionError, Exception) as e:
                print(f"Ошибка чтения: {e}")
                break

        self.running = False

    def _handle_server_packet(self, packet: Packet) -> bool:
        if packet.id == PacketIds.PING.value:
            self.on_ping_received()
            return False

        if packet.id == PacketIds.DISCONNECT.value and isinstance(
            packet, packets.Disconnect
        ):
            print(
                f"[READ] Packet ID: 0x{packet.id:02X}. Disconnect with reason: {get_translation(packet.reason)}"
            )
            self.stop()
            return False

        if self.running and not self.connected_to_server:
            # server req password
            if packet.id == PacketIds.REQUEST_PASSWORD.value:
                packet = packets.SendPassword(self.server_password)
                self.send(packet)

            # server accept password and get server slot user id
            if (
                packet.id == PacketIds.SET_USER_SLOT.value
                and isinstance(packet, packets.SetUserSlot)
                and not packet.is_server
            ):
                # save server player id
                self.player.playerID = packet.player_id

                # send player info to server
                player_info = packets.PlayerInfo(
                    player_id=self.player.playerID,
                    skin_variant=self.player.skinVariant,
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
                self.send(player_info)
                
                self.send(packets.ClientUuid(PLAYER_UUID))
                self.send(
                    packets.PlayerHp(
                        player_id=self.player.playerID,
                        hp=self.player.currHP,
                        max_hp=self.player.maxHP,
                    )
                )
                self.send(
                    packets.PlayerMana(
                        player_id=self.player.playerID,
                        mana=self.player.currMana,
                        max_mana=self.player.maxMana,
                    )
                )
                self.send(
                    packets.UpdatePlayerBuff(
                        player_id=self.player.playerID, buffs=[0] * 22
                    )
                )
                self.send(
                    packets.UpdatePlayerLoadout(
                        target_id=self.player.playerID,
                        loadout_index=0,
                        accessory_visibility=self.player.accessory_visibility
                    )
                )
                # LoadoutUpdate (0x93, id=147): accessory visibility for loadout 0
                for i in range(989):
                    self.send(
                        packets.PlayerInventorySlot(
                            player_id=self.player.playerID,
                            slot_id=i,
                            stack=0,
                            prefix=0,
                            item_netid=0,
                        )
                    )
                self.send(packets.RequestWorldData())
                # server: WORLD_INFO
                self.send(packets.RequestEssentialTiles(spawn_x=-1, spawn_y=-1))
                # server: WORLD_INFO & STATUS (load data by blocks...) & SEND_SECTION's, Unknown(0x9B) {'id': 155, 'raw': '1b012800'}, UPDATE_CHEST_ITEM's
                self.player.initialized = True

            # server say: you can spawn player
            if packet.id == PacketIds.COMPLETE_CONNECTION_SPAWN.value:
                self.send(
                    packets.SpawnPlayer(
                        player_id=self.player.playerID,
                        spawn_x=0.0,
                        spawn_y=0.0,
                        respawn_time_remaining=114,
                        player_spawn_context=2,
                    )
                )
                self.send(
                    packets.LoadNetModule(
                        variant=5,
                        body=structures.LoadNetModuleCreativeUnlocks(
                            item_id=14, sacrifice_count=0
                        ),
                    )
                )
                self.player.logged_in = True
                # then server send: NPC_HOME_UPDATE (0-29), current ANGLER_QUEST, 6 packets of SYNC_REVENGE_MARKER

            # server say: you successful connected to server
            if packet.id == PacketIds.FINISHED_CONNECTING_TO_SERVER.value:
                # then server send: LOAD_NET_MODULE (LoadNetModuleServerText messages MOTD & connect success player)
                # UPDATE_TILE_ENTITY
                self.connected_to_server = True
                
                if self.ping_thread is None:
                    self.ping_thread = threading.Thread(target=self._ping_loop, daemon=True)
                    self.ping_thread.start()
                
                # Set player teem if needed
                self.send(
                    packets.PlayerTeam(
                        player_id=self.player.playerID,
                        team=2,  # green team
                    )
                )

                # -------- repeated every minute --------
                self.send(
                    packets.PlayerZone(
                        player_id=self.player.playerID,
                        flags=0,  # 131072 / todo: check this
                    )
                )
                self.send(
                    packets.UpdatePlayerBuff(
                        player_id=self.player.playerID, buffs=[0] * 22
                    )
                )  # repeat???

                # ---0x0D UPDATE_PLAYER (0x0D) ---
                # {'player_id': 0, 'keys': 64, 'pulley': 16, 'action': 10, 'sleep_info': 0, 'selected_item': 0, 'pos': {'x': 67166.0, 'y': 6742.0, 'TILE_TO_POS_SCALE': 16.0}, 'vel': None, 'original_and_home_pos': None}

                # ---0x0D UPDATE_PLAYER (0x0D) ---
                # {'player_id': 0, 'keys': 64, 'pulley': 16, 'action': 10, 'sleep_info': 2, 'selected_item': 0, 'pos': {'x': 67166.0, 'y': 6742.0, 'TILE_TO_POS_SCALE': 16.0}, 'vel': None, 'original_and_home_pos': None}

                # --------- end repeated block

                # ---0x1B PROJECTILE_UPDATE (0x1B) ---
                # {'projectile_id': 0, 'pos': {'x': 67167.0, 'y': 6743.0, 'TILE_TO_POS_SCALE': 16.0}, 'vel': {'x': 0.0, 'y': 0.0, 'TILE_TO_POS_SCALE': 16.0}, 'owner': 0, 'ty': 398, 'flags': 0, 'ai': [0.0, 0.0], 'damage': None, 'knockback': None, 'original_damage': None, 'proj_uuid': None}

                # ---0x1B PROJECTILE_UPDATE (0x1B) ---
                # {'projectile_id': 1, 'pos': {'x': 67163.5, 'y': 6750.5, 'TILE_TO_POS_SCALE': 16.0}, 'vel': {'x': 0.0, 'y': 0.0, 'TILE_TO_POS_SCALE': 16.0}, 'owner': 0, 'ty': 18, 'flags': 0, 'ai': [0.0, 0.0], 'damage': None, 'knockback': None, 'original_damage': None, 'proj_uuid': None}

                self.send(
                    packets.UpdatePlayerLuck(
                        player_id=self.player.playerID,
                        ladybug_luck_time_remaining=0,
                        torch_luck=0,
                        luck_potion=0,
                        has_garden_gnome_nearby=0,
                    )
                )
                # Update npc names from 0 to 29
                for i in range(29):
                    self.send(
                        packets.UpdateNpcName(
                            npc_id=i, name=None, town_npc_variation_idx=None
                        )
                    )

                # ---0x9A Unknown(0x9A) ---
                # {'id': 154, 'raw': ''}

                # ---0x97 Unknown(0x97) ---
                # {'id': 151, 'raw': '7400'}

        return True

    def _writer_loop(self) -> None:
        """Поток отправки пакетов."""
        while self.running:
            try:
                packet: Packet = self.send_queue.get(timeout=1.0)
                # print(f"[WRITE] ID пакета: 0x{packet.id:02X}")
                writer = Writer()
                writer.write_byte(packet.id)
                packet.write(writer)
                payload = writer.bytes()
                len_bytes = struct.pack("<H", len(payload) + 2)
                full_packet = len_bytes + payload
                self.sock.sendall(full_packet)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                break

        self.running = False

    def send_ping(self) -> None:
        """Отправить пинг-пакет."""
        self.send(packets.Ping())

    def on_ping_received(self) -> None:
        """Обработать полученный пинг."""
        now = time.time() * 1000
        self.current_ping = int(now - self._ping_start_time)
        self._waiting_ping = False

    def update_ping(self) -> None:
        """Обновить пинг-логику."""
        now = time.time() * 1000
        if self._waiting_ping:
            self.current_ping = max(self.current_ping, int(now - self._ping_start_time))
            return
        if now - self._ping_last_sent >= 250:
            self._ping_start_time = now
            self._waiting_ping = True
            self.send_ping()
            self._ping_last_sent = now

    def _ping_loop(self) -> None:
        """Поток пинга."""
        while self.running:
            self.update_ping()
            time.sleep(0.05)

    def reset_ping(self) -> None:
        """Сбросить пинг."""
        self.current_ping = 0
        self._waiting_ping = False
        self._ping_last_sent = 0.0
        self._ping_start_time = 0.0

    def stop(self) -> None:
        """Остановить клиент."""
        self.running = False
        if self.sock:
            self.sock.close()
        if self.reader_thread:
            self.reader_thread.join(timeout=1.0)
        if self.writer_thread:
            self.writer_thread.join(timeout=1.0)
        if self.ping_thread:
            self.ping_thread.join(timeout=1.0)
