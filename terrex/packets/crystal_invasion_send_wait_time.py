from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader


class CrystalInvasionSendWaitTime(ServerPacket):
    id = MessageID.CrystalInvasionSendWaitTime

    def __init__(self, time_until_next_wave: int = 0):
        self.time_until_next_wave = time_until_next_wave

    def read(self, reader: Reader):
        self.time_until_next_wave = reader.read_int()
