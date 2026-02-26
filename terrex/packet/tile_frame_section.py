from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class TileFrameSection(ServerPacket):
    id = MessageID.TileFrameSection

    def __init__(self, start_x: int = 0, start_y: int = 0, end_x: int = 0, end_y: int = 0):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def read(self, reader: Reader):
        self.start_x = reader.read_short()
        self.start_y = reader.read_short()
        self.end_x = reader.read_short()
        self.end_y = reader.read_short()
