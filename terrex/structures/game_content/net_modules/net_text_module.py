from dataclasses import dataclass
from terrex.structures.net_string import NetworkText
from terrex.structures.rgb import Rgb
from terrex.util.streamer import Reader, Writer
from .net_module import NetServerModule


@dataclass()
class NetTextModule(NetServerModule):
    id: int = 1
    author_id: int | None = None
    text: NetworkText | None = None
    color: Rgb | None = None

    @classmethod
    def create(cls, author_id: int, text: NetworkText, color: Rgb) -> "NetTextModule":
        obj = cls()
        obj.author_id = author_id
        obj.text = text
        obj.color = color
        return obj

    def read(self, reader: Reader) -> None:
        self.author_id = reader.read_byte()
        self.text = NetworkText.read(reader)
        self.color = Rgb.read(reader)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.author_id)
        self.text.write(writer)
        self.color.write(writer)
