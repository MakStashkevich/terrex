from terrex.util.streamer import Reader, Writer
from .base import NetClientModule


class NetCraftingResponseModule(NetClientModule):
    def __init__(self, approved: bool):
        self.approved = approved

    @classmethod
    def read(cls, reader: Reader) -> 'NetCraftingResponseModule':
        approved = reader.read_bool()
        return cls(approved)

    def write(self, writer: Writer) -> None:
        writer.write_bool(self.approved)
