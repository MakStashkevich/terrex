from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID


class FinishedConnectingToServer(ServerPacket):
    id = MessageID.FinishedConnectingToServer

    def read(self, reader):
        pass
