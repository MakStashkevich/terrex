from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class MoonlordHorror(ServerPacket):
    id = MessageID.MoonlordHorror

    def __init__(self, countdown: int = 0):
        self.countdown = countdown

    def read(self, reader: Reader):
        self.countdown = reader.read_int()
