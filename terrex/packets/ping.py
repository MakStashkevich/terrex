from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class Ping(SyncPacket):
    id = MessageID.Ping

    def read(self, reader: Reader):
        pass

    def write(self, writer: Writer):
        pass
