from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds


class CompleteConnectionAndSpawn(ServerPacket):
    id = PacketIds.COMPLETE_CONNECTION_SPAWN

    def read(self, reader):
        pass

CompleteConnectionAndSpawn.register()