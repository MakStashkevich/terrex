from dataclasses import dataclass

from terrex.util.streamer import Reader, Writer


@dataclass
class Sign:
    index: int
    x: int
    y: int
    text: str

    @classmethod
    def read(cls, reader: Reader) -> 'Sign':
        return cls(
            reader.read_short(),
            reader.read_short(),
            reader.read_short(),
            reader.read_dotnet_string(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_short(self.index)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_dotnet_string(self.text)
