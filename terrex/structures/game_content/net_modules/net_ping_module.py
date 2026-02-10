from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer
from .base import NetSyncModule


class NetPingModule(NetSyncModule):
    def __init__(self, pos: Vec2):
        self.pos = pos

    @classmethod
    def read(cls, reader: Reader) -> 'NetPingModule':
        pos = Vec2.read(reader)
        return cls(pos)

    def write(self, writer: Writer) -> None:
        self.pos.write(writer)
