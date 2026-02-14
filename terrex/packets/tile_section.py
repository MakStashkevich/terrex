from typing import List, Union, Any
import zlib
from copy import deepcopy

from dataclasses import dataclass

from terrex.events.events import Event
from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


@dataclass
class TileSection:
    x_start: int
    y_start: int
    width: int
    height: int
    tiles: List["Tile"]  # pyright: ignore[reportUndefinedVariable]
    chests: List["Chest"]  # pyright: ignore[reportUndefinedVariable]
    signs: List["Sign"]  # pyright: ignore[reportUndefinedVariable]
    tile_entities: List["TileEntity"]  # pyright: ignore[reportUndefinedVariable]


def decompress_tile_block_inner(
    reader: Reader, x_start: int, y_start: int, width: int, height: int
) -> TileSection:
    from terrex.structures import Chest, Sign, Tile
    from terrex.structures.tile_entity import read_tile_entity

    tiles = [[None for _ in range(0, x_start + width)] for _ in range(0, y_start + height)]
    rle = 0
    tile = None

    for y in range(y_start, y_start + height):
        for x in range(x_start, x_start + width):
            if rle == 0:
                tile, rle = Tile.deserialize_packed(reader)
                tiles[y][x] = tile
                # print(tile)
            else:
                rle -= 1
                tiles[y][x] = deepcopy(tile)

    print("AFTER TILES OFFSET:", reader.index)
    print("NEXT 64 BYTES RAW:", reader.data[reader.index : reader.index + 64])

    n_chests = reader.read_short()
    chests = []
    for _ in range(n_chests):
        chest = Chest.read(reader)
        if 0 <= chest.x < 8000:
            chests.append(chest)

    n_signs = reader.read_short()
    signs = []
    for _ in range(n_signs):
        sign = Sign.read(reader)
        if 0 <= sign.index < 32000:
            signs.append(sign)

    n_entities = reader.read_short()
    tile_entities = [read_tile_entity(reader) for _ in range(n_entities)]

    return TileSection(
        x_start=x_start,
        y_start=y_start,
        width=width,
        height=height,
        tiles=tiles,
        chests=chests,
        signs=signs,
        tile_entities=tile_entities,
    )


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

        print(
            f"Load Section: x_start={self.x_start}, y_start={self.y_start}, width={self.width}, height={self.height}"
        )
        # Load Section: x_start=3600, y_start=150, width=200, height=150

        if self.width < 0 or self.height < 0:
            raise ValueError(f"Invalid section dimensions: {self.width}x{self.height}")

        # dimensions = width * height
        # if dimensions > 1000 * 1000:
        #     raise ValueError(f"Section dimensions too large: {width}x{height}")

        self.data = decompress_tile_block_inner(
            section_reader, self.x_start, self.y_start, self.width, self.height
        )

    def handle(self, world, player, evman):
        evman.raise_event(Event.TileUpdate, self.data)



