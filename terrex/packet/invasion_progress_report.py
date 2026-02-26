from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class InvasionProgressReport(ServerPacket):
    id = MessageID.InvasionProgressReport

    def __init__(self, progress: int = 0, max_progress: int = 0, icon: int = 0, wave: int = 0):
        self.progress = progress
        self.max_progress = max_progress
        self.icon = icon
        self.wave = wave

    def read(self, reader: Reader):
        self.progress = reader.read_int()
        self.max_progress = reader.read_int()
        self.icon = reader.read_byte()
        self.wave = reader.read_byte()
