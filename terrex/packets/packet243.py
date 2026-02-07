from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class Packet243(ServerPacket):
    id = PacketIds.PACKET243.value

    def __init__(self, buf: bytes = b""):
        self.buf = buf

    def read(self, reader: Reader):
        self.buf = reader.remaining()

    def write(self, writer: Writer):
        writer.write_bytes(self.buf)


Packet243.register()
