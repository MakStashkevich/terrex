from dataclasses import dataclass

from typing import Self, Type

from terrex.util.streamer import Reader, Writer

@dataclass
class CreativePower:
    id: int

    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        pass
