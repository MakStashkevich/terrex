from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds


class ConnectionComplete(ServerPacket):
    id = PacketIds.FINISHED_CONNECTING_TO_SERVER.value

    def read(self, reader):
        pass


ConnectionComplete.register()
