from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer


@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0

    TILE_TO_POS_SCALE: float = 16.0

    @classmethod
    def read(cls, reader: Reader) -> 'Vec2':
        return cls(
            reader.read_single(),
            reader.read_single(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_single(self.x)
        writer.write_single(self.y)

    @classmethod
    def from_tile_pos(cls, x: int, y: int) -> 'Vec2':
        return cls(
            float(x) * cls.TILE_TO_POS_SCALE,
            (float(y) - 2.625) * cls.TILE_TO_POS_SCALE,
        )
