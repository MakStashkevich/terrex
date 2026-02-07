from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds


class CrystalInvasionWipe(ServerPacket):
    id = PacketIds.CRYSTAL_INVASION_WIPE_ALL.value

    def read(self, reader):
        pass


CrystalInvasionWipe.register()
