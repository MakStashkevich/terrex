from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds


class CompleteAnglerQuest(ClientPacket):
    id = PacketIds.COMPLETE_ANGLER_QUEST_TODAY

    def write(self, writer):
        pass


CompleteAnglerQuest.register()
