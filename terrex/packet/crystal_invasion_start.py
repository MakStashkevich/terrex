from terrex.id import MessageID
from terrex.net.streamer import Writer
from terrex.packet.base import ClientPacket


class CrystalInvasionStart(ClientPacket):
    id = MessageID.CrystalInvasionStart

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
