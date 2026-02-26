from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class LiquidUpdate(SyncPacket):
    id = MessageID.LiquidUpdate

    def __init__(self, x: int = 0, y: int = 0, liquid: int = 0, liquid_type: int = 0):
        self.x = x
        self.y = y
        self.liquid = liquid
        self.liquid_type = liquid_type

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.liquid = reader.read_byte()
        self.liquid_type = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_byte(self.liquid)
        writer.write_byte(self.liquid_type)
