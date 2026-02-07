from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class PaintWall(SyncPacket):
    id = PacketIds.PAINT_WALL.value

    def __init__(self, x: int = 0, y: int = 0, color: int = 0):
        self.x = x
        self.y = y
        self.color = color

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.color = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_byte(self.color)


PaintWall.register()
