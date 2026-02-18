from terrex.packet.base import ClientPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class RequestChestOpen(ClientPacket):
    id = MessageID.RequestChestOpen

    def __init__(self, tile_x: int = 0, tile_y: int = 0):
        self.tile_x = tile_x
        self.tile_y = tile_y

    def write(self, writer: Writer):
        writer.write_short(self.tile_x)
        writer.write_short(self.tile_y)

    def read(self, reader: Reader) -> None:
        self.tile_x = reader.read_short()
        self.tile_y = reader.read_short()
