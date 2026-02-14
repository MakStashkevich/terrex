from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID


class AnglerQuestFinished(ClientPacket):
    id = MessageID.AnglerQuestFinished

    def write(self, writer):
        pass
