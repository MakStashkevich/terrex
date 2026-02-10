from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds


class Placeholder(Packet):
    id = PacketIds.PLACEHOLDER_67

    def read(self, reader):
        pass

    def write(self, writer):
        pass


Placeholder.register()
