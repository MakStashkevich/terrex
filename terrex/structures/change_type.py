from enum import IntEnum

from terrex.util.streamer import Reader, Writer


class ChangeType(IntEnum):
    NONE = 0
    LAVA_WATER = 1
    HONEY_WATER = 2
    HONEY_LAVA = 3

    @classmethod
    def read(cls, reader: Reader) -> 'ChangeType':
        return cls(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.value)