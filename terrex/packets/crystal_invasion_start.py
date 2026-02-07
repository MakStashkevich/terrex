from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class CrystalInvasionStart(ClientPacket):
    id = PacketIds.CRYSTAL_INVASION_START.value

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)


CrystalInvasionStart.register()
