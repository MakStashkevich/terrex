from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class Ping(SyncPacket):
    id = PacketIds.PING

    def read(self, reader: Reader):
        pass

    def write(self, writer: Writer):
        pass


Ping.register()
