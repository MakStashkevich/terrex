import socket
import struct
import threading
import queue
import time
from typing import Optional

from terrex import packets
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
        self, host: str, port: int, protocol: int, player: Player, world: World, evman: EventManager
    ):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.player = player
        self.world = world
        self._evman = evman

        self.sock: Optional[socket.socket] = None
        self.send_queue = queue.Queue()
        self.recv_queue = queue.Queue()
        self.running = False
        self.reader_thread: Optional[threading.Thread] = None
        self.writer_thread: Optional[threading.Thread] = None

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

        # Handshake
        self.send(packets.Connect(self.protocol))
        self.send(
            packets.PlayerInfo(
                self.player.name,
                self.player.hairStyle,
                self.player.skinColor,
                self.player.hairColor,
                self.player.eyeColor,
                self.player.shirtColor,
                self.player.undershirtColor,
                self.player.pantsColor,
                self.player.shoeColor,
            )
        )
        self.send(packets.ClientUuid(PLAYER_UUID))
        self.send(packets.PlayerHp(player_id=self.player.playerID, hp=self.player.currHP, max_hp=self.player.maxHP))
        self.send(packets.PlayerMana(player_id=self.player.playerID, mana=self.player.currMana, max_mana=self.player.maxMana))
        self.send(packets.UpdatePlayerBuff(player_id=self.player.playerID, buffs=[0] * 22))
        for i in range(260):
            self.send(
                packets.PlayerInventorySlot(
                    player_id=self.player.playerID, slot_id=i, stack=0, prefix=0, item_netid=0
                )
            )
        self.send(packets.RequestWorldData())
        self.send(packets.RequestEssentialTiles(spawn_x=-1, spawn_y=-1))
        self.send(
            packets.SpawnPlayer(
                player_id=self.player.playerID,
                spawn_x=-1.0,
                spawn_y=-1.0,
                respawn_time_remaining=0,
                player_spawn_context=0,
            )
        )

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
                    
                    if packet_id == 2 and isinstance(packet, packets.Disconnect):
                        print(f"[READ] Packet ID: 0x{packet_id:02X}. Disconnect with reason: {get_translation(packet.reason)}")
                        self.stop()
                        continue

                    self.recv_queue.put(packet)
                else:
                    print(f"Неизвестный ID пакета: 0x{packet_id:02X}, name: {PacketIds[packet_id].name}")
            except (ConnectionError, Exception) as e:
                print(f"Ошибка чтения: {e}")
                break

        self.running = False

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

    def stop(self) -> None:
        """Остановить клиент."""
        self.running = False
        if self.sock:
            self.sock.close()
        if self.reader_thread:
            self.reader_thread.join(timeout=1.0)
        if self.writer_thread:
            self.writer_thread.join(timeout=1.0)
