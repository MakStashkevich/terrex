from terrex.packet.base import ClientPacket
from terrex.id import MessageID


class AnglerQuestFinished(ClientPacket):
    id = MessageID.AnglerQuestFinished

    def write(self, writer):
        pass
