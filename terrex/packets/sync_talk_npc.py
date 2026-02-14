from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class SyncTalkNPC(SyncPacket):
    id = MessageID.SyncTalkNPC

    def __init__(self, player_id: int = 0, npc_talk_target: int = 0):
        self.player_id = player_id
        self.npc_talk_target = npc_talk_target

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.npc_talk_target = reader.read_short()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.npc_talk_target)
