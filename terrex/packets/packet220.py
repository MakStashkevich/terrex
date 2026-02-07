from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class Packet220(ServerPacket):
    id = PacketIds.PACKET220.value

    def __init__(self, buf: bytes = b""):
        self.buf = buf

    def read(self, reader: Reader):
        self.buf = reader.remaining()

    def write(self, writer: Writer):
        writer.write_bytes(self.buf)


Packet220.register()
