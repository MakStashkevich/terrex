from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class SyncPlayerChest(SyncPacket):
    id = MessageID.SyncPlayerChest

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
