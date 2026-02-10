from typing import List, Union, Any
import zlib
from copy import deepcopy

from dataclasses import dataclass

from terrex.events.events import Event
from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


@dataclass
class SendSection:
    x_start: int
    y_start: int
    width: int
    height: int
    tiles: List["Tile"] # pyright: ignore[reportUndefinedVariable]
    # chests: List["Chest"] # pyright: ignore[reportUndefinedVariable]
    # signs: List["Sign"] # pyright: ignore[reportUndefinedVariable]
    # tile_entities: List["TileEntity"] # pyright: ignore[reportUndefinedVariable]


def read_decompressed_section(reader: Reader) -> SendSection:
    from terrex.structures import Chest, Sign, Tile
    from terrex.structures.tile_entity import read_tile_entity
    
    x_start = reader.read_int()
    y_start = reader.read_int()
    width = reader.read_short()
    height = reader.read_short()

    if width < 0 or height < 0:
        raise ValueError(f"Invalid section dimensions: {width}x{height}")

    # dimensions = width * height
    # if dimensions > 1000 * 1000:
    #     raise ValueError(f"Section dimensions too large: {width}x{height}")
    
    tiles = [[None for _ in range(width)] for _ in range(height)]
    rle = 0
    tile = None

    for y in range(height):
        for x in range(width):
            if rle == 0:
                tile, rle = Tile.deserialize_packed(reader)
                tiles[y][x] = tile
                print(tile)
            else:
                rle -= 1
                tiles[y][x] = deepcopy(tile)

    print("AFTER TILES OFFSET:", reader.index)
    print("NEXT 64 BYTES RAW:", reader.data[reader.index:reader.index+64])

    # n_chests = reader.read_short()
    # chests = []
    # for _ in range(n_chests):
    #     chest = Chest.read(reader)
    #     if 0 <= chest.x < 8000:
    #         chests.append(chest)

    # n_signs = reader.read_short()
    # signs = []
    # for _ in range(n_signs):
    #     sign = Sign.read(reader)
    #     if 0 <= sign.index < 32000:
    #         signs.append(sign)

    # n_entities = reader.read_short()
    # tile_entities = [read_tile_entity(reader) for _ in range(n_entities)]

    return SendSection(
        x_start=x_start,
        y_start=y_start,
        width=width,
        height=height,
        tiles=tiles,
        # chests=chests,
        # signs=signs,
        # tile_entities=tile_entities
    )


class PacketSendSection(ServerPacket):
    id = PacketIds.SEND_SECTION.value

    def read(self, reader: Reader) -> None:
        compressed_data = reader.remaining()
        decompressed = zlib.decompress(compressed_data, -zlib.MAX_WBITS)
        section_reader = Reader(decompressed)

        self.data = read_decompressed_section(section_reader)
        self.x_start = self.data.x_start
        self.y_start = self.data.y_start

    def handle(self, world, player, evman):
        evman.raise_event(Event.TileUpdate, self.data)

PacketSendSection.register()
