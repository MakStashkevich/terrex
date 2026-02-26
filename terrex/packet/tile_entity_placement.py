from enum import IntEnum

from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import ClientPacket


class TileEntityType(IntEnum):
    TRAINING_DUMMY = 0
    ITEM_FRAME = 1
    LOGIC_SENSOR = 2

    @classmethod
    def read(cls, reader: Reader) -> 'TileEntityType':
        return cls(reader.read_byte())

    def write(self, writer: Writer):
        writer.write_byte(self.value)


class TileEntityPlacement(ClientPacket):
    id = MessageID.TileEntityPlacement

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        tile_entity_type: TileEntityType = TileEntityType.TRAINING_DUMMY,
    ):
        self.x = x
        self.y = y
        self.tile_entity_type = tile_entity_type

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        self.tile_entity_type.write(writer)

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.tile_entity_type = TileEntityType.read(reader)
