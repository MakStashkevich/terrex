from terrex.packet.base import ClientPacket
from terrex.id import MessageID
from terrex.net.streamer import Writer


class BugCatching(ClientPacket):
    id = MessageID.BugCatching

    def __init__(self, npc_id: int = 0, player_id: int = 0):
        self.npc_id = npc_id
        self.player_id = player_id

    def write(self, writer: Writer):
        writer.write_short(self.npc_id)
        writer.write_byte(self.player_id)
