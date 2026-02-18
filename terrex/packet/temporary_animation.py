from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader


class TemporaryAnimation(ServerPacket):
    id = MessageID.TemporaryAnimation

    def __init__(self, animation_type: int = 0, tile_type: int = 0, x: int = 0, y: int = 0):
        self.animation_type = animation_type
        self.tile_type = tile_type
        self.x = x
        self.y = y

    def read(self, reader: Reader):
        self.animation_type = reader.read_short()
        self.tile_type = reader.read_ushort()
        self.x = reader.read_short()
        self.y = reader.read_short()
