from enum import IntEnum

from terrex.util.streamer import Reader, Writer


class LiquidType(IntEnum):
    NONE = 0
    WATER = 1
    LAVA = 2
    HONEY = 3
    SHIMMER = 4

    @classmethod
    def read(cls, reader: Reader) -> 'LiquidType':
        return cls(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.value)