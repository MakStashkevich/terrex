from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader


class CreateTemporaryAnimation(ServerPacket):
    id = PacketIds.CREATE_TEMPORARY_ANIMATION.value

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


CreateTemporaryAnimation.register()
