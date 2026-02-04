from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class RequestWorldData(Packet):
    id = PacketIds.REQUEST_WORLD_DATA.value

    def read(self, reader: Reader):
        pass

    def write(self, writer: Writer):
        pass

RequestWorldData.register()