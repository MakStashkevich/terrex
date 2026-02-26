from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class Ping(SyncPacket):
    id = MessageID.Ping

    def read(self, reader: Reader):
        pass

    def write(self, writer: Writer):
        pass
