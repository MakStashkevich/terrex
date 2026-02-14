from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader


class MoonlordHorror(ServerPacket):
    id = MessageID.MoonlordHorror

    def __init__(self, countdown: int = 0):
        self.countdown = countdown

    def read(self, reader: Reader):
        self.countdown = reader.read_int()
