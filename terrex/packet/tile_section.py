import zlib

from terrex.event.types import TileSectionUpdateEvent
from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.world.world import World


def decompress_tile_block_inner(reader: Reader, world: World, x_start: int, y_start: int, width: int, height: int) -> list['Tile']:
    from terrex.net.structure.chest import Chest
    from terrex.net.structure.sign import Sign
    from terrex.net.structure.tile import Tile
    from terrex.entity.tile_entity import read_tile_entity

    tile_list: list[Tile] = []
    tile: Tile | None = None
    rle: int = 0
    for y in range(y_start, y_start + height):
        for x in range(x_start, x_start + width):
            if rle == 0:
                tile, rle = Tile.deserialize_packed(reader, world, x, y)
                tile_list.append(tile)
            else:
                rle -= 1
                new_tile = World.tiles.get(x, y) or Tile()
                new_tile.copy_from(tile)
                World.tiles.set(x, y, new_tile)
                tile_list.append(tile)

    print("AFTER TILES OFFSET:", reader.index)
    print("NEXT 64 BYTES RAW:", reader.data[reader.index : reader.index + 64])

    n_chests = reader.read_short()
    for _ in range(n_chests):
        chest = Chest.read(reader)
        if 0 <= chest.index < 8000:
            World.chest[chest.index] = chest

    n_signs = reader.read_short()
    for _ in range(n_signs):
        sign = Sign.read(reader)
        if 0 <= sign.index < 32000:
            World.sign[sign.index] = sign

    n_entities = reader.read_short()
    for _ in range(n_entities):
        World.tile_entity.append(read_tile_entity(reader))
        
    return tile_list


class TileSection(ServerPacket):
    id = MessageID.TileSection

    def read(self, reader: Reader) -> None:
        compressed_data = reader.remaining()
        decompressed = zlib.decompress(compressed_data, -zlib.MAX_WBITS)
        section_reader = Reader(decompressed)

        self.x_start = section_reader.read_int()
        self.y_start = section_reader.read_int()
        self.width = section_reader.read_short()
        self.height = section_reader.read_short()

        print(f"Load Section: x_start={self.x_start}, y_start={self.y_start}, width={self.width}, height={self.height}")
        # Load Section: x_start=3600, y_start=150, width=200, height=150

        if self.width < 0 or self.height < 0:
            raise ValueError(f"Invalid section dimensions: {self.width}x{self.height}")

        # dimensions = width * height
        # if dimensions > 1000 * 1000:
        #     raise ValueError(f"Section dimensions too large: {width}x{height}")

        # todo: add props world
        self.tiles = decompress_tile_block_inner(section_reader, World, self.x_start, self.y_start, self.width, self.height)

    async def handle(self, world, player, evman):
        await evman.raise_event(TileSectionUpdateEvent(self, self.tiles))
