from dataclasses import dataclass
from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer
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
        self.pos.write(writer)
