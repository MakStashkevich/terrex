from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader


class PoofOfSmoke(ServerPacket):
    id = PacketIds.POOF_SMOKE

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()


PoofOfSmoke.register()
