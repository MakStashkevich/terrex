from dataclasses import dataclass
from typing import Any

from terrex.util.streamer import Reader, Writer


@dataclass
class Vec2:
    x: float
    y: float

    TILE_TO_POS_SCALE: float = 16.0

    @classmethod
    def read(cls, reader: Reader) -> 'Vec2':
        return cls(
            reader.read_float(),
            reader.read_float(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_float(self.x)
        writer.write_float(self.y)

    @classmethod
    def from_tile_pos(cls, x: int, y: int) -> 'Vec2':
        return cls(
            float(x) * cls.TILE_TO_POS_SCALE,
            (float(y) - 2.625) * cls.TILE_TO_POS_SCALE,
        )