from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds


class CompleteConnectionAndSpawn(ServerPacket):
    id = PacketIds.COMPLETE_CONNECTION_SPAWN.value

    def read(self, reader):
        pass

CompleteConnectionAndSpawn.register()