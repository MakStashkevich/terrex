from terrex.net.bits_byte import BitsByte
from terrex.net.enum.mode import NetMode
from terrex.net.tile_npc_data import TileNPCData
from terrex.net.tile_stack import TileStack
from terrex.packet.base import SyncPacket
from terrex.id import MessageID, TileChangeType, TileID
from terrex.net.structure.tile import Tile
from terrex.net.streamer import Reader, Writer
from terrex.world.world import World

tile_data = TileNPCData()


class AreaTileChange(SyncPacket):
    id = MessageID.AreaTileChange

    def __init__(
        self,
        tile_y: int = 0,
        tile_x: int = 0,
        height: int = 0,
        width: int = 0,
        change_type: TileChangeType = TileChangeType.NoneValue,
        tiles: TileStack | None = None,
    ):
        self.tile_y: int = tile_y
        self.tile_x: int = tile_x
        # self.tile_x = max(0, min(self.tile_x, World.max_tiles_x - self.width - 1))
        # self.tile_y = max(0, min(self.tile_y, World.max_tiles_y - self.height - 1))
        self.height: int = height
        self.width: int = width
        self.change_type: TileChangeType = change_type
        self.tiles: TileStack = tiles or TileStack()

    def read(self, reader: Reader):
        self.tile_x = reader.read_short()
        self.tile_y = reader.read_short()
        self.width = reader.read_byte()
        self.height = reader.read_byte()
        self.change_type = TileChangeType(reader.read_byte())

        self.tiles = TileStack()
        for x in range(self.tile_x, self.tile_x + self.width):
            for y in range(self.tile_y, self.tile_y + self.height):
                bits1 = BitsByte(reader.read_byte())
                bits2 = BitsByte(reader.read_byte())
                bits3 = BitsByte(reader.read_byte())

                tile_color = reader.read_byte() if bits2[2] else 0
                wall_color = reader.read_byte() if bits2[3] else 0

                tile_type = 0
                frameX = frameY = 0
                if bits1[0]:
                    tile_type = reader.read_ushort()

                    if tile_type > TileID.Count:
                        raise ValueError(f"Corrupted tile type {tile_type}")

                    if tile_data.tileFrameImportant[tile_type]:
                        frameX = reader.read_short()
                        frameY = reader.read_short()

                wall = reader.read_ushort() if bits1[2] else 0
                liquid = liquid_type = 0
                if bits1[3] and reader.net_mode == NetMode.SERVER:
                    liquid = reader.read_byte()
                    liquid_type = reader.read_byte()

                tile = Tile()
                tile.active = bits1[0]
                tile.wall = wall
                tile.liquid = liquid
                tile.liquid_type = liquid_type
                tile.wire = bits1[4]
                tile.half_brick = bits1[5]
                tile.actuator = bits1[6]
                tile.inactive = bits1[7]
                tile.wire2 = bits2[0]
                tile.wire3 = bits2[1]
                tile.wire4 = bits2[7]
                tile.slope = (int(bits2) >> 4) & 0x07
                tile.color = tile_color
                tile.wall_color = wall_color
                tile.fullbright_block = bits3[0]
                tile.fullbright_wall = bits3[1]
                tile.invisible_block = bits3[2]
                tile.invisible_wall = bits3[3]
                tile.type = tile_type
                tile.frame_x = frameX
                tile.frame_y = frameY

                self.tiles.set(x, y, tile)

    async def handle(self, world, player, evman):
        for (x, y), tile in self.tiles.items():
            if not isinstance(tile, Tile):
                continue
            world.tiles.set(x, y, tile)

    def write(self, writer: Writer):
        writer.write_short(self.tile_x)
        writer.write_short(self.tile_y)
        writer.write_byte(self.width)
        writer.write_byte(self.height)
        writer.write_byte(self.change_type)

        for x in range(self.tile_x, self.tile_x + self.width):
            for y in range(self.tile_y, self.tile_y + self.height):
                tile = self.tiles.get(x, y)
                if not tile:
                    tile = Tile()

                bits1 = BitsByte()
                bits2 = BitsByte()
                bits3 = BitsByte()

                bits1[0] = tile.active
                bits1[2] = tile.wall > 0
                bits1[3] = tile.liquid > 0 and writer.net_mode == NetMode.SERVER
                bits1[4] = tile.wire
                bits1[5] = tile.half_brick
                bits1[6] = tile.actuator
                bits1[7] = tile.inactive

                bits2[0] = tile.wire2
                bits2[1] = tile.wire3
                bits2[2] = tile.active and tile.color > 0
                bits2[3] = tile.wall > 0 and tile.wall_color > 0
                bits2[7] = tile.wire4
                bits2_value = (int(bits2) & 0x0F) | ((tile.slope & 0x07) << 4)
                bits2 = BitsByte(bits2_value)

                bits3[0] = tile.fullbright_block
                bits3[1] = tile.fullbright_wall
                bits3[2] = tile.invisible_block
                bits3[3] = tile.invisible_wall

                writer.write_byte(int(bits1))
                writer.write_byte(int(bits2))
                writer.write_byte(int(bits3))

                if bits2[2]:
                    writer.write_byte(tile.color)
                if bits2[3]:
                    writer.write_byte(tile.wall_color)

                if tile.active:
                    writer.write_ushort(tile.type)
                    if tile_data.tileFrameImportant[tile.type]:
                        writer.write_short(tile.frame_x)
                        writer.write_short(tile.frame_y)

                if tile.wall > 0:
                    writer.write_ushort(tile.wall)
                if tile.liquid > 0 and writer.net_mode == NetMode.SERVER:
                    writer.write_byte(tile.liquid)
                    writer.write_byte(tile.liquid_type)
