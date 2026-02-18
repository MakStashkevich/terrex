from terrex.packet.base import ServerPacket
from terrex.id import MessageID


class RequestPassword(ServerPacket):
    id = MessageID.RequestPassword

    def read(self, reader):
        pass
