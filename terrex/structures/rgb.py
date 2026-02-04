from dataclasses import dataclass
from typing import Any

from terrex.util.streamer import Reader, Writer


@dataclass
class Rgb:
    r: int
    g: int
    b: int

    @classmethod
    def read(cls, reader: Reader) -> 'Rgb':
        return cls(
            reader.read_byte(),
            reader.read_byte(),
            reader.read_byte(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.r)
        writer.write_byte(self.g)
        writer.write_byte(self.b)