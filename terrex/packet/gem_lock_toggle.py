from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import ClientPacket


class GemLockToggle(ClientPacket):
    id = MessageID.GemLockToggle

    def __init__(self, x: int = 0, y: int = 0, on: bool = False):
        self.x = x
        self.y = y
        self.on = on

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_bool(self.on)

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.on = reader.read_bool()
