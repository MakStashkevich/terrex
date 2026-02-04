from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds


class RequestPassword(Packet):
    id = PacketIds.REQUEST_PASSWORD.value

    def read(self, reader):
        pass

    def write(self, writer):
        pass

RequestPassword.register()