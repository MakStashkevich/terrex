from terrex.id import MessageID
from terrex.packet.base import ClientPacket


class AnglerQuestFinished(ClientPacket):
    id = MessageID.AnglerQuestFinished

    def write(self, writer):
        pass
