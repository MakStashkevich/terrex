from dataclasses import dataclass

from terrex.net.bestiary import Bestiary
from terrex.net.streamer import Reader, Writer

from .net_module import NetServerModule


@dataclass()
class NetBestiaryModule(NetServerModule):
    id: int = 4
    bestiary: Bestiary | None = None

    @classmethod
    def create(cls, bestiary: Bestiary) -> "NetBestiaryModule":
        obj = cls()
        obj.bestiary = bestiary
        return obj

    def read(self, reader: Reader) -> 'NetBestiaryModule':
        self.bestiary = Bestiary.read(reader)

    def write(self, writer: Writer) -> None:
        self.bestiary.write(writer)
