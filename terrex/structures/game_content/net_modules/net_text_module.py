from terrex.structures.net_string import NetworkText
from terrex.structures.rgb import Rgb
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class NetTextModule(NetServerModule):
    def __init__(self, author_id: int, text: NetworkText, color: Rgb):
        self.author_id = author_id
        self.text = text
        self.color = color

    @classmethod
    def read(cls, reader: Reader) -> 'NetTextModule':
        author_id = reader.read_byte()
        text = NetworkText.read(reader)
        color = Rgb.read(reader)
        return cls(author_id, text, color)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.author_id)
        self.text.write(writer)
        self.color.write(writer)
