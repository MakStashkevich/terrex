from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class PlaceObject(SyncPacket):
    id = MessageID.PlaceObject

    def __init__(self, x: int = 0, y: int = 0, ty: int = 0, style: int = 0, alternate: int = 0, random: int = 0, direction: bool = False):
        self.x = x
        self.y = y
        self.ty = ty
        self.style = style
        self.alternate = alternate
        self.random = random
        self.direction = direction

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.ty = reader.read_short()
        self.style = reader.read_short()
        self.alternate = reader.read_byte()
        self.random = reader.read_sbyte()
        self.direction = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.ty)
        writer.write_short(self.style)
        writer.write_byte(self.alternate)
        writer.write_sbyte(self.random)
        writer.write_bool(self.direction)
