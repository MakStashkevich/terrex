from dataclasses import dataclass
from typing import Any

from terrex.util.streamer import Reader, Writer


@dataclass
class Chest:
    x: int
    y: int
    style: int
    name: str

    @classmethod
    def read(cls, reader: Reader) -> 'Chest':
        return cls(
            reader.read_short(),
            reader.read_short(),
            reader.read_short(),
            reader.read_terraria_string(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.style)
        writer.write_string(self.name)