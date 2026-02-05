from typing import Optional, Tuple, List
import struct

from dataclasses import dataclass, field

from terrex.util.streamer import Reader, Writer
from terrex.structures.liquid_type import LiquidType

TILE_FRAME_IMPORTANT = [
    0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1,
    0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0,
    1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1,
    1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
    0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0,
    1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1,
    1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,
]

def is_important(ty: int) -> bool:
    if 0 <= ty < len(TILE_FRAME_IMPORTANT):
        return TILE_FRAME_IMPORTANT[ty] != 0
    return False


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


@dataclass
class Tile:
    flags: int = 0  # u16 bitflags
    color: Optional[int] = None  # u8
    wall_color: Optional[int] = None  # u8
    ty: Optional[int] = None  # u16
    frame: Optional[Tuple[int, int]] = None  # i16, i16
    wall: Optional[int] = None  # u16
    liquid: Optional[Tuple[int, LiquidType]] = None  # u8, LiquidType

    @classmethod
    def deserialize_packed(cls, reader: Reader) -> Tuple['Tile', int]:
        flags_bytes = [reader.read_byte(), 0, 0]
        if flags_bytes[0] & 0x01 != 0:
            flags_bytes[1] = reader.read_byte()
            if flags_bytes[1] & 0x01 != 0:
                flags_bytes[2] = reader.read_byte()

        tile_flags = 0  # u16

        ty = None
        frame = None
        color = None
        if flags_bytes[0] & 0x02 != 0:
            tile_flags |= TileFlags.ACTIVE  # ACTIVE
            if flags_bytes[0] & 0x20 != 0:
                ty_val = reader.read_ushort()
            else:
                ty_val = reader.read_byte()
            ty = ty_val

            if is_important(ty_val):
                frame = (reader.read_short(), reader.read_short())

            if flags_bytes[2] & 0x08 != 0:
                tile_flags |= TileFlags.HAS_COLOR  # HAS_COLOR
                color = reader.read_byte()

        wall = None
        wall_color = None
        if flags_bytes[0] & 0x04 != 0:
            tile_flags |= TileFlags.HAS_WALL  # HAS_WALL
            wall_val = reader.read_byte()
            if flags_bytes[2] & 0x10 != 0:
                tile_flags |= TileFlags.HAS_WALL_COLOR  # HAS_WALL_COLOR
                wall_color = reader.read_byte()
            wall = wall_val

        liquid = None
        liquid_code = (flags_bytes[0] & 0x18) >> 3
        if liquid_code == 1:
            liquid = (reader.read_byte(), LiquidType.Water)
            tile_flags |= TileFlags.HAS_LIQUID  # HAS_LIQUID
        elif liquid_code == 2:
            liquid = (reader.read_byte(), LiquidType.Lava)
            tile_flags |= TileFlags.HAS_LIQUID
        elif liquid_code == 3:
            liquid = (reader.read_byte(), LiquidType.Honey)
            tile_flags |= TileFlags.HAS_LIQUID

        # Wires
        if flags_bytes[1] & 0x02 != 0:
            tile_flags |= TileFlags.WIRE1  # WIRE1
        if flags_bytes[1] & 0x04 != 0:
            tile_flags |= TileFlags.WIRE2  # WIRE2
        if flags_bytes[1] & 0x08 != 0:
            tile_flags |= TileFlags.WIRE3  # WIRE3
        if flags_bytes[2] & 0x20 != 0:
            tile_flags |= TileFlags.WIRE4  # WIRE4

        # Shape
        shape = (flags_bytes[1] & 0x70) >> 4
        if shape == 1:
            tile_flags |= TileFlags.HALF_BRICK  # HALF_BRICK
        elif shape == 2:
            tile_flags |= TileFlags.SLOPE1  # SLOPE1
        elif shape == 3:
            tile_flags |= TileFlags.SLOPE2  # SLOPE2
        elif shape == 4:
            tile_flags |= TileFlags.SLOPE3  # SLOPE3

        if flags_bytes[2] & 0x02 != 0:
            tile_flags |= TileFlags.ACTUATOR  # ACTUATOR
        if flags_bytes[2] & 0x04 != 0:
            tile_flags |= TileFlags.INACTIVE  # INACTIVE

        if flags_bytes[2] & 0x40 != 0:
            if wall is not None:
                wall |= (reader.read_byte() << 8)
            else:
                raise ValueError("Wall high byte without wall")

        # RLE
        rle_code = (flags_bytes[0] & 0xc0) >> 6
        if rle_code == 0:
            rle = 0
        elif rle_code == 1:
            rle = reader.read_byte()
        else:
            rle = reader.read_ushort()

        return cls(
            flags=tile_flags,
            color=color,
            wall_color=wall_color,
            ty=ty,
            frame=frame,
            wall=wall,
            liquid=liquid
        ), rle

    @classmethod
    def read(cls, reader: Reader) -> 'Tile':
        # Fallback unpacked read
        flags = reader.read_ushort()
        color = reader.read_byte() if flags & TileFlags.HAS_COLOR else None
        wall_color = reader.read_byte() if flags & TileFlags.HAS_WALL_COLOR else None
        ty = reader.read_ushort() if flags & TileFlags.ACTIVE else None
        frame = (reader.read_short(), reader.read_short()) if ty and is_important(ty) else None
        wall = reader.read_ushort() if flags & TileFlags.HAS_WALL else None
        liquid = (reader.read_byte(), LiquidType.read(reader)) if flags & TileFlags.HAS_LIQUID else None
        return cls(flags=flags, color=color, wall_color=wall_color, ty=ty, frame=frame, wall=wall, liquid=liquid)

    def write(self, writer: Writer) -> None:
        # TODO: implement serialization
        pass
