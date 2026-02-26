from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class ChestName(SyncPacket):
    id = MessageID.ChestName

    def __init__(self, chest_id: int = 0, x: int = 0, y: int = 0, name: str = ""):
        self.chest_id = chest_id
        self.x = x
        self.y = y
        self.name = name

    def read(self, reader: Reader):
        self.chest_id = reader.read_short()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.name = reader.read_dotnet_string()

    def write(self, writer: Writer):
        writer.write_short(self.chest_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_dotnet_string(self.name)
