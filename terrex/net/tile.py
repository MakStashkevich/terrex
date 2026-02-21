from dataclasses import dataclass

from terrex.id.LiquidID import LiquidID
from terrex.id import LiquidID
from terrex.net.tile_npc_data import TileNPCData
from terrex.net.streamer import Reader, Writer
from terrex.world.world import World

tile_data = TileNPCData()


@dataclass
class Tile:
    type: int = 0  # ushort
    wall: int = 0  # ushort

    # metadata
    liquid: int = 0  # byte
    s_tile_header: int = 0  # ushort
    b_tile_header: int = 0  # byte
    b_tile_header2: int = 0  # byte
    b_tile_header3: int = 0  # byte
    frame_x: int = 0  # short
    frame_y: int = 0  # short

    @classmethod
    def deserialize_packed(cls, reader: Reader, tile_x: int, tile_y: int) -> tuple["Tile", int]:
        tile = World.tiles.get(tile_x, tile_y)
        if tile:
            tile.clear_everything()
        else:
            tile = cls()
            World.tiles.set(tile_x, tile_y, tile)

        flags_bytes = [reader.read_byte(), 0, 0]
        if flags_bytes[0] & 0x01:
            flags_bytes[1] = reader.read_byte()
            if flags_bytes[1] & 0x01:
                flags_bytes[2] = reader.read_byte()
                if flags_bytes[2] & 0x01:
                    flags_bytes.append(reader.read_byte())  # num4

        # ACTIVE tile
        is_active = tile.active
        if flags_bytes[0] & 0x02:
            tile.active = True
            old_tile_type = tile.type
            if flags_bytes[0] & 0x20:
                low = reader.read_byte()
                high = reader.read_byte()
                ty_val = (high << 8) | low
            else:
                ty_val = reader.read_byte()
            tile.type = ty_val

            if tile_data.tileFrameImportant[ty_val]:
                tile.frame_x = reader.read_short()
                tile.frame_y = reader.read_short()
            elif not is_active or tile.type != old_tile_type:
                tile.frame_x = -1
                tile.frame_y = -1

            if len(flags_bytes) > 3 and flags_bytes[3] & 0x08:
                tile.color = reader.read_byte()

        # WALL
        if flags_bytes[0] & 0x04:
            tile.wall = reader.read_byte()
            if len(flags_bytes) > 3 and flags_bytes[3] & 0x10:
                tile.wall_color = reader.read_byte()

        # LIQUID
        liquid_code = (flags_bytes[0] & 0x18) >> 3
        if liquid_code != 0:
            tile.liquid = reader.read_byte()
            if len(flags_bytes) > 3 and flags_bytes[3] & 0x80:
                tile.shimmer = True
            elif liquid_code > 1:
                if liquid_code != 2:
                    tile.honey = True
                else:
                    tile.lava = True

        # Wires
        if flags_bytes[1] & 0x02:
            tile.wire = True
        if flags_bytes[1] & 0x04:
            tile.wire2 = True
        if flags_bytes[1] & 0x08:
            tile.wire3 = True
        if flags_bytes[2] & 0x20:
            tile.wire4 = True

        # Shape
        shape = (flags_bytes[1] & 0x70) >> 4
        if shape != 0:  # and World.tileSolid[tile.type]
            if shape != 1:
                tile.slope = int(shape - 1)
            else:
                tile.half_brick = True

        if flags_bytes[2] & 0x02:
            tile.actuator = True
        if flags_bytes[2] & 0x04:
            tile.inactive = True

        # Wall high byte
        if flags_bytes[2] & 0x40:
            tile.wall = (reader.read_byte() << 8) | tile.wall

        # num4 flags (extra)
        num4 = flags_bytes[3] if len(flags_bytes) > 3 else 0
        if num4 > 1:
            if num4 & 0x02:
                tile.invisible_block = True
            if num4 & 0x04:
                tile.invisible_wall = True
            if num4 & 0x08:
                tile.fullbright_block = True
            if num4 & 0x10:
                tile.fullbright_wall = True

        # RLE
        rle_code = (flags_bytes[0] & 0xC0) >> 6
        if rle_code == 0:
            rle = 0
        elif rle_code == 1:
            rle = reader.read_byte()
        else:  # 2 or 3
            rle = reader.read_short()

        return (tile, rle)

    def copy_from(self, from_tile: 'Tile') -> None:
        self.type = from_tile.type
        self.wall = from_tile.wall
        self.liquid = from_tile.liquid
        self.s_tile_header = from_tile.s_tile_header
        self.b_tile_header = from_tile.b_tile_header
        self.b_tile_header2 = from_tile.b_tile_header2
        self.b_tile_header3 = from_tile.b_tile_header3
        self.frame_x = from_tile.frame_x
        self.frame_y = from_tile.frame_y

    def clear_everything(self) -> None:
        self.type = 0
        self.wall = 0
        self.clear_metadata()

    def clear_metadata(self) -> None:
        self.liquid = 0
        self.s_tile_header = 0
        self.b_tile_header = 0
        self.b_tile_header2 = 0
        self.b_tile_header3 = 0
        self.frame_x = 0
        self.frame_y = 0

    # --- active (бит 5) ---
    @property
    def active(self) -> bool:
        """Возвращает True, если установлен бит 5 (32)"""
        return (self.s_tile_header & 32) == 32

    @active.setter
    def active(self, value: bool) -> None:
        """Устанавливает или сбрасывает бит 5 (32)"""
        if value:
            self.s_tile_header |= 32
        else:
            self.s_tile_header &= 0xFFFF ^ 32  # 65503

    # --- color (биты 0-4) ---
    @property
    def color(self) -> int:
        """Возвращает значение цвета из битов 0–4"""
        return self.s_tile_header & 31  # 0b11111

    @color.setter
    def color(self, value: int) -> None:
        """Устанавливает цвет в биты 0–4, не затрагивая остальные"""
        self.s_tile_header = (self.s_tile_header & 0xFFFF ^ 31) | (value & 31)

    @property
    def wall_color(self) -> int:
        """Биты 0–4 (маска 0b11111 = 31)"""
        return self.b_tile_header & 31

    @wall_color.setter
    def wall_color(self, value: int) -> None:
        # очищаем биты 0–4 (оставляем 5–7), затем вставляем новое значение
        self.b_tile_header = (self.b_tile_header & 0b11100000) | (value & 31)
        self.b_tile_header &= 0xFF  # гарантируем диапазон byte

    @property
    def water(self) -> bool:
        return self.liquid_type == LiquidID.Water

    # --- lava (биты 5–6 = 01) ---
    @property
    def lava(self) -> bool:
        return (self.b_tile_header & 96) == 32

    @lava.setter
    def lava(self, value: bool) -> None:
        if not value:
            self.b_tile_header &= 0b11011111  # 223
        else:
            self.b_tile_header = (self.b_tile_header & 0b10011111) | 32
        self.b_tile_header &= 0xFF

    # --- honey (биты 5–6 = 10) ---
    @property
    def honey(self) -> bool:
        return (self.b_tile_header & 96) == 64

    @honey.setter
    def honey(self, value: bool) -> None:
        if not value:
            self.b_tile_header &= 0b10111111  # 191
        else:
            self.b_tile_header = (self.b_tile_header & 0b10011111) | 64
        self.b_tile_header &= 0xFF

    # --- shimmer (биты 5 и 6 = 96) ---
    @property
    def shimmer(self) -> bool:
        return (self.b_tile_header & 96) == 96

    @shimmer.setter
    def shimmer(self, value: bool) -> None:
        if not value:
            self.b_tile_header &= 0b10011111  # 159
        else:
            self.b_tile_header = (self.b_tile_header & 0b10011111) | 96
        self.b_tile_header &= 0xFF

    # --- liquid_type (0–3) ---
    @property
    def liquid_type(self) -> int:
        return (self.b_tile_header & 96) >> 5

    @liquid_type.setter
    def liquid_type(self, liquid_type: int) -> None:
        if liquid_type == LiquidID.Water:
            self.b_tile_header &= 0b10011111  # 159
        elif liquid_type == LiquidID.Lava:
            self.lava = True
        elif liquid_type == LiquidID.Honey:
            self.honey = True
        elif liquid_type == LiquidID.Shimmer:
            self.shimmer = True

    # skipLiquid (бит 4 b_tile_header3)
    @property
    def skip_liquid(self) -> bool:
        return (self.b_tile_header3 & 16) == 16

    @skip_liquid.setter
    def skip_liquid(self, value: bool) -> None:
        if value:
            self.b_tile_header3 |= 16
        else:
            self.b_tile_header3 &= 0b11101111  # 239
        self.b_tile_header3 &= 0xFF

    # slope (биты 12–14 s_tile_header)
    @property
    def slope(self) -> int:
        return (self.s_tile_header & 0b0111000000000000) >> 12  # 28672

    @slope.setter
    def slope(self, value: int) -> None:
        self.s_tile_header = (self.s_tile_header & 0b1000111111111111) | ((value & 7) << 12)  # 36863
        self.s_tile_header &= 0xFFFF

    @property
    def top_slope(self) -> bool:
        s = self.slope
        return s == 1 or s == 2

    # wallFrameNumber (биты 6–7 b_tile_header2)
    @property
    def wall_frame_number(self) -> int:
        return (self.b_tile_header2 & 0b11000000) >> 6

    @wall_frame_number.setter
    def wall_frame_number(self, value: int) -> None:
        self.b_tile_header2 = (self.b_tile_header2 & 0b00111111) | ((value & 3) << 6)
        self.b_tile_header2 &= 0xFF

    # wallFrameX (биты 0–3 b_tile_header2)
    @property
    def wall_frame_x(self) -> int:
        return (self.b_tile_header2 & 0b00001111) * 36

    @wall_frame_x.setter
    def wall_frame_x(self, value: int) -> None:
        self.b_tile_header2 = (self.b_tile_header2 & 0b11110000) | ((value // 36) & 15)
        self.b_tile_header2 &= 0xFF

    # wallFrameY (биты 0–2 b_tile_header3)
    @property
    def wall_frame_y(self) -> int:
        return (self.b_tile_header3 & 0b00000111) * 36

    @wall_frame_y.setter
    def wall_frame_y(self, value: int) -> None:
        self.b_tile_header3 = (self.b_tile_header3 & 0b11111000) | ((value // 36) & 7)
        self.b_tile_header3 &= 0xFF

    # wires (s_tile_header и b_tile_header)
    @property
    def wire(self) -> bool:
        return (self.s_tile_header & 128) == 128

    @wire.setter
    def wire(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 128
        else:
            self.s_tile_header &= 0b1111111101111111  # 65407
        self.s_tile_header &= 0xFFFF

    @property
    def wire2(self) -> bool:
        return (self.s_tile_header & 256) == 256

    @wire2.setter
    def wire2(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 256
        else:
            self.s_tile_header &= 0b1111111011111111  # 65279
        self.s_tile_header &= 0xFFFF

    @property
    def wire3(self) -> bool:
        return (self.s_tile_header & 512) == 512

    @wire3.setter
    def wire3(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 512
        else:
            self.s_tile_header &= 0b1111110111111111  # 65023
        self.s_tile_header &= 0xFFFF

    @property
    def wire4(self) -> bool:
        return (self.b_tile_header & 128) == 128

    @wire4.setter
    def wire4(self, value: bool) -> None:
        if value:
            self.b_tile_header |= 128
        else:
            self.b_tile_header &= 0b01111111
        self.b_tile_header &= 0xFF

    # frameNumber (биты 4–5 b_tile_header2)
    @property
    def frame_number(self) -> int:
        return (self.b_tile_header2 & 0b00110000) >> 4  # 48

    @frame_number.setter
    def frame_number(self, value: int) -> None:
        self.b_tile_header2 = (self.b_tile_header2 & 0b11001111) | ((value & 3) << 4)  # 207
        self.b_tile_header2 &= 0xFF

    # fullbrightBlock (бит 7 b_tile_header3)
    @property
    def fullbright_block(self) -> bool:
        return (self.b_tile_header3 & 128) == 128

    @fullbright_block.setter
    def fullbright_block(self, value: bool) -> None:
        if value:
            self.b_tile_header3 |= 128
        else:
            self.b_tile_header3 &= 0b01111111  # 127
        self.b_tile_header3 &= 0xFF

    # fullbrightWall (бит 15 s_tile_header)
    @property
    def fullbright_wall(self) -> bool:
        return (self.s_tile_header & 32768) == 32768

    @fullbright_wall.setter
    def fullbright_wall(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 32768
        else:
            self.s_tile_header &= 0b0111111111111111  # 32767
        self.s_tile_header &= 0xFFFF

    # halfBrick (бит 10 s_tile_header)
    @property
    def half_brick(self) -> bool:
        return (self.s_tile_header & 1024) == 1024

    @half_brick.setter
    def half_brick(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 1024
        else:
            self.s_tile_header &= 0b1111101111111111  # 64511
        self.s_tile_header &= 0xFFFF

    # active (бит 5 s_tile_header)
    @property
    def active(self) -> bool:
        return (self.s_tile_header & 32) == 32

    @active.setter
    def active(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 32
        else:
            self.s_tile_header &= 0b1111111111011111  # 65503
        self.s_tile_header &= 0xFFFF

    # actuator (бит 11 s_tile_header)
    @property
    def actuator(self) -> bool:
        return (self.s_tile_header & 2048) == 2048

    @actuator.setter
    def actuator(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 2048
        else:
            self.s_tile_header &= 0b1111011111111111  # 63487
        self.s_tile_header &= 0xFFFF

    # anyLiquid variants
    @property
    def any_honey(self) -> bool:
        return self.liquid > 0 and self.honey

    @property
    def any_lava(self) -> bool:
        return self.liquid > 0 and self.lava

    @property
    def any_shimmer(self) -> bool:
        return self.liquid > 0 and self.shimmer

    @property
    def any_water(self) -> bool:
        return self.liquid > 0 and self.water

    # blockType
    @property
    def block_type(self) -> int:
        if self.half_brick:
            return 1
        s = self.slope
        if s > 0:
            s += 1
        return s

    # slope helpers
    @property
    def bottom_slope(self) -> bool:
        s = self.slope
        return s == 3 or s == 4

    @property
    def left_slope(self) -> bool:
        s = self.slope
        return s == 2 or s == 4

    @property
    def right_slope(self) -> bool:
        s = self.slope
        return s == 1 or s == 3

    @property
    def top_slope(self) -> bool:
        s = self.slope
        return s == 1 or s == 2

    # checkingLiquid (бит 3 b_tile_header3)
    @property
    def checking_liquid(self) -> bool:
        return (self.b_tile_header3 & 8) == 8

    @checking_liquid.setter
    def checking_liquid(self, value: bool) -> None:
        if value:
            self.b_tile_header3 |= 8
        else:
            self.b_tile_header3 &= 0b11110111  # 247
        self.b_tile_header3 &= 0xFF

    # inActive (бит 6 s_tile_header)
    @property
    def inactive(self) -> bool:
        return (self.s_tile_header & 64) == 64

    @inactive.setter
    def inactive(self, value: bool) -> None:
        if value:
            self.s_tile_header |= 64
        else:
            self.s_tile_header &= 0b1111111110111111  # 65471
        self.s_tile_header &= 0xFFFF

    # invisibleBlock (бит 5 b_tile_header3)
    @property
    def invisible_block(self) -> bool:
        return (self.b_tile_header3 & 32) == 32

    @invisible_block.setter
    def invisible_block(self, value: bool) -> None:
        if value:
            self.b_tile_header3 |= 32
        else:
            self.b_tile_header3 &= 0b11011111  # 223
        self.b_tile_header3 &= 0xFF

    # invisibleWall (бит 6 b_tile_header3)
    @property
    def invisible_wall(self) -> bool:
        return (self.b_tile_header3 & 64) == 64

    @invisible_wall.setter
    def invisible_wall(self, value: bool) -> None:
        if value:
            self.b_tile_header3 |= 64
        else:
            self.b_tile_header3 &= 0b10111111  # 191
        self.b_tile_header3 &= 0xFF

    def __str__(self) -> str:
        return f"Tile(type={self.type}, active={self.active}, wall={self.wall}, slope={self.slope}, fX={self.frame_x}, fY={self.frame_y}"
