from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer
from terrex.net.structure.liquid import Liquid

from .net_module import NetServerModule


@dataclass()
class NetLiquidModule(NetServerModule):
    id: int = 0
    liquids: list[Liquid] | None = None

    @classmethod
    def create(cls, liquids: list[Liquid]) -> "NetLiquidModule":
        obj = cls()
        obj.liquids = liquids
        return obj

    def read(self, reader: Reader) -> None:
        count = reader.read_ushort()
        self.liquids = [Liquid.read(reader) for _ in range(count)]

    def write(self, writer: Writer) -> None:
        if self.liquids is None:
            raise ValueError("liquids must not be None")
        writer.write_ushort(len(self.liquids))
        for liquid in self.liquids:
            liquid.write(writer)
