from typing import List, Union, Any
import zlib

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
    chests: List["Chest"] # pyright: ignore[reportUndefinedVariable]
    signs: List["Sign"] # pyright: ignore[reportUndefinedVariable]
    tile_entities: List["TileEntity"] # pyright: ignore[reportUndefinedVariable]


def read_decompressed_section(reader: Reader) -> SendSection:
    from terrex.structures import Chest, Sign, Tile
    from terrex.structures.tile_entity import read_tile_entity
    
    x_start = reader.read_int()
    y_start = reader.read_int()
    width = reader.read_short()
    height = reader.read_short()

    if width < 0 or height < 0:
        raise ValueError(f"Invalid section dimensions: {width}x{height}")

    dimensions = width * height
    if dimensions > 1000 * 1000:
        raise ValueError(f"Section dimensions too large: {width}x{height}")

    tiles: List[Tile] = []
    rle = 0

    for _ in range(dimensions):
        if rle > 0:
            tiles.append(tiles[-1])
            rle -= 1
        else:
            tile, rle_new = Tile.deserialize_packed(reader)
            tiles.append(tile)
            rle = rle_new

    n_chests = reader.read_ushort()
    chests = [Chest.read(reader) for _ in range(n_chests)]

    n_signs = reader.read_ushort()
    signs = [Sign.read(reader) for _ in range(n_signs)]

    n_entities = reader.read_ushort()
    tile_entities = [read_tile_entity(reader) for _ in range(n_entities)]

    return SendSection(
        x_start=x_start,
        y_start=y_start,
        width=width,
        height=height,
        tiles=tiles,
        chests=chests,
        signs=signs,
        tile_entities=tile_entities
    )


class PacketSendSection(ServerPacket):
    id = PacketIds.SEND_SECTION.value

    def read(self, reader: Reader) -> None:
        # self.raw = reader.remaining()
        self.x_start = None
        self.y_start = None
        
        is_compressed = reader.read_bool()
        self.check_comressed = True
        if is_compressed:
            self.compressed = True

            remaining = reader.remaining()
            decompressed = zlib.decompress(remaining)
            section_reader = Reader(decompressed)
            self.data = read_decompressed_section(section_reader)
            
            self.x_start = self.data.x_start
            self.y_start = self.data.y_start
        else:
            self.compressed = False
            
            self.data = read_decompressed_section(reader)
            
            self.x_start = self.data.x_start
            self.y_start = self.data.y_start
        
        self.is_ended = True
            
    def handle(self, world, player, evman):
        evman.raise_event(Event.TileUpdate, self.data)

PacketSendSection.register()
