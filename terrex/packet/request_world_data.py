from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import ClientPacket


class RequestWorldData(ClientPacket):
    id = MessageID.RequestWorldData

    def write(self, writer: Writer):
        pass

    def read(self, reader: Reader) -> None:
        pass
