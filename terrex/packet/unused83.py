from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class Unused83(ServerPacket):
    # SetNPCKillCount
    id = MessageID.Unused83

    def __init__(self, npc_type: int = 0, kill_count: int = 0):
        self.npc_type = npc_type
        self.kill_count = kill_count

    def read(self, reader: Reader):
        self.npc_type = reader.read_short()
        self.kill_count = reader.read_int()
