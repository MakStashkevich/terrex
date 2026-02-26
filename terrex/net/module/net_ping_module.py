from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer
from terrex.net.structure.vec2 import Vec2

from .net_module import NetSyncModule


@dataclass()
class NetPingModule(NetSyncModule):
    id: int = 2
    pos: Vec2 | None = None

    @classmethod
    def create(cls, pos: Vec2) -> "NetPingModule":
        obj = cls()
        obj.pos = pos
        return obj

    def read(self, reader: Reader) -> None:
        self.pos = Vec2.read(reader)

    def write(self, writer: Writer) -> None:
        if self.pos is None:
            raise ValueError("pos must be Vec2 and not None")
        self.pos.write(writer)
