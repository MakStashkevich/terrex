import struct
import traceback

from terrex.packets.base import Packet, packet_registry
from terrex.structures.id import MessageID
from terrex.structures.net_mode import NetMode
from terrex.util.streamer import Reader


class UnknownPacket(Packet):
    id: int = -1

    def __init__(self, pid: int):
        super().__init__()
        self.id = pid
        self.raw = b""

    def read(self, reader: Reader):
        self.raw = reader.remaining()


class IncrementalParser:
    def __init__(self):
        """Initialize the incremental parser with an empty buffer."""
        self.buffer: bytearray = bytearray()

    def feed(self, data: bytes) -> None:
        """Append raw data to the internal buffer for incremental parsing."""
        self.buffer.extend(data)

    def next(self, net_mode: NetMode) -> Packet | None:
        """Extract the next complete packet from the buffer.

        Protocol format:
        - First 2 bytes: little-endian uint16 TOTAL_LENGTH (includes length field itself)
        - Next (TOTAL_LENGTH - 2) bytes: PAYLOAD, starting with 1-byte packet ID
        """
        while len(self.buffer) >= 2:
            length_total = struct.unpack("<H", self.buffer[:2])[0]
            if len(self.buffer) < length_total:
                break

            packet_full = self.buffer[:length_total]
            self.buffer = self.buffer[length_total:]

            payload = packet_full[2:]
            if len(payload) == 0:
                continue  # Skip empty payloads

            reader = Reader(payload, protocol_version=999, net_mode=net_mode)
            try:
                packet_id = reader.read_byte()  # First byte of payload is packet ID
            except IndexError:
                continue  # Incomplete payload

            packet_cls = packet_registry.get(packet_id)
            if packet_cls:
                packet = packet_cls()
            else:
                packet = UnknownPacket(packet_id)

            try:
                packet.read(reader)
            except Exception as e:
                print(traceback.format_exc())
                try:
                    name = MessageID(packet_id).name
                except ValueError:
                    name = "UNKNOWN"
                print(f"Error reading packet {packet_id:02X}, name: {name}: {e}")
                # Fallback already handled by UnknownPacket.read if applicable

            return packet
        return None
