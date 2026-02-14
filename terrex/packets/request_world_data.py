from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class RequestWorldData(ClientPacket):
    id = MessageID.RequestWorldData

    def write(self, writer: Writer):
        pass

    def read(self, reader: Reader) -> None:
        pass
