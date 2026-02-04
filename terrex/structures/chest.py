from dataclasses import dataclass
from typing import Any

from terrex.util.streamer import Reader, Writer


@dataclass
class Chest:
    index: int
    x: int
    y: int
    name: str

    @classmethod
    def read(cls, reader: Reader) -> 'Chest':
        return cls(
            reader.read_ushort(),
            reader.read_short(),
            reader.read_short(),
            reader.read_string(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_ushort(self.index)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_string(self.name)