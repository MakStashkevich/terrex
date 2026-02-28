from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer

TILE_TO_POS_SCALE: float = 16.0


@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0

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
            float(x) * TILE_TO_POS_SCALE,
            (float(y) - 2.625) * TILE_TO_POS_SCALE,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: object) -> bool:
        return not self == other

    def distance_to(self, other: 'Vec2') -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5
