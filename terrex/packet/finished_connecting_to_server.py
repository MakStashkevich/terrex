from terrex.packet.base import ServerPacket
from terrex.id import MessageID


class FinishedConnectingToServer(ServerPacket):
    id = MessageID.FinishedConnectingToServer

    def read(self, reader):
        pass
