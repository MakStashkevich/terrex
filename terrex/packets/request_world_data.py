from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class RequestWorldData(ClientPacket):
    id = PacketIds.REQUEST_WORLD_DATA.value

    def write(self, writer: Writer):
        pass

    def read(self, reader: Reader) -> None:
        pass

RequestWorldData.register()