from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader


class UpdateGoodEvil(ServerPacket):
    id = MessageID.UpdateGoodEvil

    def __init__(self, good: int = 0, evil: int = 0, crimson: int = 0):
        self.good = good
        self.evil = evil
        self.crimson = crimson

    def read(self, reader: Reader):
        self.good = reader.read_byte()
        self.evil = reader.read_byte()
        self.crimson = reader.read_byte()
