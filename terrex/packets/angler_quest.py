from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class AnglerQuest(ServerPacket):
    id = PacketIds.ANGLER_QUEST.value

    def __init__(self, quest: int = 0, completed: bool = False):
        self.quest = quest
        self.completed = completed

    def read(self, reader: Reader):
        self.quest = reader.read_byte()
        self.completed = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_byte(self.quest)
        writer.write_bool(self.completed)


AnglerQuest.register()
