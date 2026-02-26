from terrex.id import MessageID
from terrex.packet.base import ServerPacket


class FinishedConnectingToServer(ServerPacket):
    id = MessageID.FinishedConnectingToServer

    def read(self, reader):
        pass
