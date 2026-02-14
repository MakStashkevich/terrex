from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID


class RequestPassword(ServerPacket):
    id = MessageID.RequestPassword

    def read(self, reader):
        pass
