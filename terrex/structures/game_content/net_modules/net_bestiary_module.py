from terrex.structures.game_content.bestiary import Bestiary
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class NetBestiaryModule(NetServerModule):
    def __init__(self, bestiary: Bestiary):
        self.bestiary = bestiary

    @classmethod
    def read(cls, reader: Reader) -> 'NetBestiaryModule':
        bestiary = Bestiary.read(reader)
        return cls(bestiary)

    def write(self, writer: Writer) -> None:
        self.bestiary.write(writer)
