from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer

 

class SpawnTileData(ClientPacket):
    id = MessageID.SpawnTileData

    def __init__(self, spawn_x: int = -1, spawn_y: int = -1):
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

    def write(self, writer: Writer):
        writer.write_short(self.spawn_x)
        writer.write_short(self.spawn_y)

    def read(self, reader: Reader) -> None:
        self.spawn_x = reader.read_short()
        self.spawn_y = reader.read_short()

