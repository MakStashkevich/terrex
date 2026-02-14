from terrex.structures.id import MessageID
from terrex.packets.base import ServerPacket
from terrex.util.streamer import Reader, Writer


class TileEntitySharing(ServerPacket):
    id = MessageID.TileEntitySharing

    def __init__(self):
        self.tile_entity_id: int = 0
        self.update_flag: bool = True
        self.tile_entity_type: int = 0
        self.x: int = 0
        self.y: int = 0

    def read(self, reader: Reader) -> None:
        self.tile_entity_id = reader.read_int()
        self.update_flag = reader.read_bool()
        if not self.update_flag:
            self.tile_entity_type = reader.read_byte()
            self.x = reader.read_short()
            self.y = reader.read_short()

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Server does not send UpdateTileEntity (client-bound packet only)")

