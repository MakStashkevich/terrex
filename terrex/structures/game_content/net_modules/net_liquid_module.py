from typing import List
from terrex.structures.game_content.liquid import Liquid
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class NetLiquidModule(NetServerModule):
    def __init__(self, liquids: List[Liquid]):
        self.liquids = liquids

    @classmethod
    def read(cls, reader: Reader) -> 'NetLiquidModule':
        count = reader.read_ushort()
        liquids = [Liquid.read(reader) for _ in range(count)]
        return cls(liquids)

    def write(self, writer: Writer) -> None:
        writer.write_ushort(len(self.liquids))
        for liquid in self.liquids:
            liquid.write(writer)
