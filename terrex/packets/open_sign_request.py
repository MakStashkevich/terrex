from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class OpenSignRequest(ClientPacket):
    id = MessageID.OpenSignRequest

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)

    def read(self, reader: Reader) -> None:
        self.x = reader.read_short()
        self.y = reader.read_short()
