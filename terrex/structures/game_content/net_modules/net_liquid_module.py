from typing import List
from dataclasses import dataclass
from terrex.structures.game_content.liquid import Liquid
from terrex.util.streamer import Reader, Writer
from .net_module import NetServerModule


@dataclass()
class NetLiquidModule(NetServerModule):
    id: int = 0
    liquids: List[Liquid] | None = None

    @classmethod
    def create(cls, liquids: List[Liquid]) -> "NetLiquidModule":
        obj = cls()
        obj.liquids = liquids
        return obj

    def read(self, reader: Reader) -> None:
        count = reader.read_ushort()
        self.liquids = [Liquid.read(reader) for _ in range(count)]

    def write(self, writer: Writer) -> None:
        writer.write_ushort(len(self.liquids))
        for liquid in self.liquids:
            liquid.write(writer)
