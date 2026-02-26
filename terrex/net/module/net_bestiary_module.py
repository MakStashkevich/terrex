from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer
from terrex.net.structure.bestiary import Bestiary

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

    def read(self, reader: Reader) -> None:
        self.bestiary = Bestiary.read(reader)

    def write(self, writer: Writer) -> None:
        if self.bestiary is None:
            raise ValueError("bestiary must not be None")
        self.bestiary.write(writer)
