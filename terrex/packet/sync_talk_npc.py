from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class SyncTalkNPC(SyncPacket):
    id = MessageID.SyncTalkNPC

    def __init__(self, player_id: int = 0, npc_talk_target: int = 0):
        self.player_id = player_id
        self.npc_talk_id = npc_talk_target

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.npc_talk_id = reader.read_short()
        
    async def handle(self, world, player, evman):
        if not self.player_id in world.players:
            return
        current_player = world.players[self.player_id]
        current_player.npc_talk_id = self.npc_talk_id

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.npc_talk_id)
