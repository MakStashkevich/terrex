import struct
from typing import Optional

from terrex.packets.base import registry, Packet
from terrex.packets.base import Packet
from terrex.util.streamer import Reader

class UnknownPacket(Packet):
    def __init__(self, pid: int):
        super().__init__()
        self.id = pid
        self.raw = b""

    def read(self, reader: Reader):
        self.raw = reader.remaining()


class IncrementalParser:
    def __init__(self):
        self.buffer: bytearray = bytearray()

    def feed(self, data: bytes) -> None:
        self.buffer.extend(data)

    def next(self) -> Optional[Packet]:
        while len(self.buffer) >= 2:
            length_bytes = self.buffer[:2]
            length = struct.unpack("<H", length_bytes)[0]
            if len(self.buffer) < 2 + length:
                break

            packet_full = self.buffer[:2 + length]
            self.buffer = self.buffer[2 + length:]

            payload = packet_full[2:]
            if len(payload) == 0:
                continue

            reader = Reader(payload)
            try:
                packet_id = reader.read_byte()
            except IndexError:
                continue

            packet_cls = registry.get(packet_id)
            if packet_cls is None:
                continue

            packet = packet_cls()
            try:
                packet.read(reader)
                return packet
            except Exception:
                packet = UnknownPacket(packet_id)
                packet.read(reader)
                return packet
        return None
