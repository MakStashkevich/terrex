from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class AnglerQuests(ClientPacket):
    id = PacketIds.NUMBER_ANGLER_QUESTS_COMPLETED.value

    def __init__(self, player_id: int = 0, angler_quests_completed: int = 0, golfer_score: int = 0):
        self.player_id = player_id
        self.angler_quests_completed = angler_quests_completed
        self.golfer_score = golfer_score

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_int(self.angler_quests_completed)
        writer.write_int(self.golfer_score)


AnglerQuests.register()
