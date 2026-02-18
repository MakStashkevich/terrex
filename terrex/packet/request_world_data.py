from terrex.packet.base import ClientPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class RequestWorldData(ClientPacket):
    id = MessageID.RequestWorldData

    def write(self, writer: Writer):
        pass

    def read(self, reader: Reader) -> None:
        pass
