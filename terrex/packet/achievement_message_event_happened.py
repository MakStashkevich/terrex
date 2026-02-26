from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class AchievementMessageEventHappened(ServerPacket):
    id = MessageID.AchievementMessageEventHappened

    def __init__(self, event_id: int = 0):
        self.event_id = event_id

    def read(self, reader: Reader) -> None:
        self.event_id = reader.read_short()
