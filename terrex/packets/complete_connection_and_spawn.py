from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds


class CompleteConnectionAndSpawn(Packet):
    id = PacketIds.COMPLETE_CONNECTION_SPAWN.value

    def read(self, reader):
        pass

    def write(self, writer):
        pass

CompleteConnectionAndSpawn.register()