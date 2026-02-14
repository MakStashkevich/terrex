from terrex.packets.base import SyncPacket
from terrex.structures.change_type import ChangeType
from terrex.structures.id import MessageID
from terrex.structures.tile import Tile
from terrex.util.streamer import Reader, Writer


class AreaTileChange(SyncPacket):
    id = MessageID.AreaTileChange

    def __init__(self, tile_y: int = 0, tile_x: int = 0, height: int = 0, width: int = 0, change_type: ChangeType = ChangeType.NONE, tiles: list[Tile] = None):
        self.tile_y = tile_y
        self.tile_x = tile_x
        self.height = height
        self.width = width
        self.change_type = change_type
        self.tiles = tiles or []

    def read(self, reader: Reader):
        self.tile_y = reader.read_short()
        self.tile_x = reader.read_short()
        self.height = reader.read_byte()
        self.width = reader.read_byte()
        self.change_type = ChangeType.read(reader)
        tiles = []
        needed = self.width * self.height
        while len(tiles) < needed:
            tile, rle = Tile.deserialize_packed(reader)
            tiles.extend([tile] * (rle + 1))
        self.tiles = tiles[:needed]

    def write(self, writer: Writer):
        writer.write_short(self.tile_y)
        writer.write_short(self.tile_x)
        writer.write_byte(self.height)
        writer.write_byte(self.width)
        self.change_type.write(writer)
        for tile in self.tiles:
            tile.write(writer)
