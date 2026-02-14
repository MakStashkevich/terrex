from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class QuestsCountSync(ClientPacket):
    id = MessageID.QuestsCountSync

    def __init__(self, player_id: int = 0, angler_quests_completed: int = 0, golfer_score: int = 0):
        self.player_id = player_id
        self.angler_quests_completed = angler_quests_completed
        self.golfer_score = golfer_score

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_int(self.angler_quests_completed)
        writer.write_int(self.golfer_score)

 

