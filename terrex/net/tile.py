from dataclasses import dataclass

from terrex.id.LiquidID import LiquidID
from terrex.id import LiquidID
from terrex.net.tile_npc_data import TileNPCData
from terrex.net.streamer import Reader, Writer

tile_data = TileNPCData()


class TileFlags:
    ACTIVE = 0x0001
    LIGHTED = 0x0002
    HAS_WALL = 0x0004
    HAS_LIQUID = 0x0008
    WIRE1 = 0x0010
    HALF_BRICK = 0x0020
    ACTUATOR = 0x0040
    INACTIVE = 0x0080
    WIRE2 = 0x0100
    WIRE3 = 0x0200
    HAS_COLOR = 0x0400
    HAS_WALL_COLOR = 0x0800
    SLOPE1 = 0x1000
    SLOPE2 = 0x2000
    SLOPE3 = 0x4000
    WIRE4 = 0x8000
    INVISIBLE_BLOCK = 0x10000
    INVISIBLE_WALL = 0x20000
    FULLBRIGHT_BLOCK = 0x40000
    FULLBRIGHT_WALL = 0x80000


@dataclass
class Tile:
    flags: int = 0  # u16 bitflags
    color: int | None = None  # u8
    wall_color: int | None = None  # u8
    ty: int | None = None  # u16
    frame: tuple[int, int] | None = None  # i16, i16
    wall: int | None = None  # u16
    liquid: tuple[int, LiquidID] | None = None  # u8, LiquidID

    @classmethod
    def deserialize_packed(cls, reader: Reader) -> tuple["Tile", int]:
        flags_bytes = [reader.read_byte(), 0, 0]
        if flags_bytes[0] & 0x01:
            flags_bytes[1] = reader.read_byte()
            if flags_bytes[1] & 0x01:
                flags_bytes[2] = reader.read_byte()
                if flags_bytes[2] & 0x01:
                    flags_bytes.append(reader.read_byte())  # num4

        tile_flags = 0
        tile_type = None
        frame = (-1, -1)
        color = None
        wall = None
        wall_color = None
        liquid = None

        # ACTIVE tile
        if flags_bytes[0] & 0x02:
            tile_flags |= TileFlags.ACTIVE
            if flags_bytes[0] & 0x20:
                low = reader.read_byte()
                high = reader.read_byte()
                ty_val = (high << 8) | low
            else:
                ty_val = reader.read_byte()
            tile_type = ty_val

            if tile_data.tileFrameImportant[ty_val]:
                frame = (reader.read_short(), reader.read_short())
            else:  # elif tile.active() || type_type_new != tyle_type_old
                frame = (-1, -1)

            if len(flags_bytes) > 3 and flags_bytes[3] & 0x08:
                tile_flags |= TileFlags.HAS_COLOR
                color = reader.read_byte()

        # WALL
        if flags_bytes[0] & 0x04:
            tile_flags |= TileFlags.HAS_WALL
            wall = reader.read_byte()
            if len(flags_bytes) > 3 and flags_bytes[3] & 0x10:
                tile_flags |= TileFlags.HAS_WALL_COLOR
                wall_color = reader.read_byte()

        # LIQUID
        liquid_code = (flags_bytes[0] & 0x18) >> 3
        if liquid_code != 0:
            amt = reader.read_byte()
            if len(flags_bytes) > 3 and flags_bytes[3] & 0x80:
                liq_type = LiquidID.Shimmer
            elif liquid_code == 2:
                liq_type = LiquidID.Lava
            elif liquid_code == 3:
                liq_type = LiquidID.Honey
            else:
                liq_type = LiquidID.Water
            liquid = (amt, liq_type)
            tile_flags |= TileFlags.HAS_LIQUID

        # Wires
        if flags_bytes[1] & 0x02:
            tile_flags |= TileFlags.WIRE1
        if flags_bytes[1] & 0x04:
            tile_flags |= TileFlags.WIRE2
        if flags_bytes[1] & 0x08:
            tile_flags |= TileFlags.WIRE3
        if flags_bytes[2] & 0x20:
            tile_flags |= TileFlags.WIRE4

        # Shape
        shape = (flags_bytes[1] & 0x70) >> 4
        if shape == 1:
            tile_flags |= TileFlags.HALF_BRICK
        elif shape == 2:
            tile_flags |= TileFlags.SLOPE1
        elif shape == 3:
            tile_flags |= TileFlags.SLOPE2
        elif shape == 4:
            tile_flags |= TileFlags.SLOPE3

        if flags_bytes[2] & 0x02:
            tile_flags |= TileFlags.ACTUATOR
        if flags_bytes[2] & 0x04:
            tile_flags |= TileFlags.INACTIVE

        # Wall high byte
        if flags_bytes[2] & 0x40:
            wall = (reader.read_byte() << 8) | (wall if wall else 0)

        # num4 flags (extra)
        num4 = flags_bytes[3] if len(flags_bytes) > 3 else 0
        if num4 > 1:
            if num4 & 0x02:
                tile_flags |= TileFlags.INVISIBLE_BLOCK
            if num4 & 0x04:
                tile_flags |= TileFlags.INVISIBLE_WALL
            if num4 & 0x08:
                tile_flags |= TileFlags.FULLBRIGHT_BLOCK
            if num4 & 0x10:
                tile_flags |= TileFlags.FULLBRIGHT_WALL

        # RLE
        rle_code = (flags_bytes[0] & 0xC0) >> 6
        if rle_code == 0:
            rle = 0
        elif rle_code == 1:
            rle = reader.read_byte()
        else:  # 2 or 3
            rle = reader.read_short()

        return (
            cls(
                flags=tile_flags,
                color=color,
                wall_color=wall_color,
                ty=tile_type,
                frame=frame,
                wall=wall,
                liquid=liquid,
            ),
            rle,
        )

    @classmethod
    def read(cls, reader: Reader) -> "Tile":
        # Fallback unpacked read
        flags = reader.read_ushort()
        color = reader.read_byte() if flags & TileFlags.HAS_COLOR else None
        wall_color = reader.read_byte() if flags & TileFlags.HAS_WALL_COLOR else None
        ty = reader.read_ushort() if flags & TileFlags.ACTIVE else None
        frame = (reader.read_short(), reader.read_short()) if ty and tile_data.tileFrameImportant[ty] else None
        wall = reader.read_ushort() if flags & TileFlags.HAS_WALL else None
        liquid = (reader.read_byte(), LiquidID(reader.read_byte())) if flags & TileFlags.HAS_LIQUID else None
        return cls(
            flags=flags,
            color=color,
            wall_color=wall_color,
            ty=ty,
            frame=frame,
            wall=wall,
            liquid=liquid,
        )

    def write(self, writer: Writer) -> None:
        # TODO: implement serialization
        pass
