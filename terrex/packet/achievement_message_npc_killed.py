from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader


class AchievementMessageNPCKilled(ServerPacket):
    id = MessageID.AchievementMessageNPCKilled

    def __init__(self, npc_id: int = 0):
        self.npc_id = npc_id

    def read(self, reader: Reader) -> None:
        self.npc_id = reader.read_short()

