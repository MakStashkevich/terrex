from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds


class RequestPassword(ServerPacket):
    id = PacketIds.REQUEST_PASSWORD.value

    def read(self, reader):
        pass

RequestPassword.register()