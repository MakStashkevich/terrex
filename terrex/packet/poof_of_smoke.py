from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader


class PoofOfSmoke(ServerPacket):
    id = MessageID.PoofOfSmoke

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()
