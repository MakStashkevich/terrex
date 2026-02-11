from enum import IntEnum
from typing import List, Self

from terrex.util.streamer import Reader, Writer


class NetworkTextMode(IntEnum):
    LITERAL = 0
    FORMATTABLE = 1
    LOCALIZATION_KEY = 2

    @classmethod
    def read(cls, reader: Reader) -> 'NetworkTextMode':
        return cls(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.value)


class NetworkText:
    def __init__(self, mode: NetworkTextMode = NetworkTextMode.LITERAL, text: str = "", substitutions: List[Self] = None):
        self.mode = mode
        self.text = text
        self.substitutions = substitutions or []

    @classmethod
    def read(cls, reader: Reader) -> 'NetworkText':
        mode = NetworkTextMode.read(reader)
        text = reader.read_dotnet_string()
        substitutions = []
        if mode != NetworkTextMode.LITERAL:
            count = reader.read_byte()
            for _ in range(count):
                substitutions.append(NetworkText.read(reader))
        return cls(mode, text, substitutions)

    def write(self, writer: Writer) -> None:
        self.mode.write(writer)
        writer.write_dotnet_string(self.text)
        if self.mode != NetworkTextMode.LITERAL:
            writer.write_byte(len(self.substitutions))
            for sub in self.substitutions:
                sub.write(writer)