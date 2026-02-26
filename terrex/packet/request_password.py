from terrex.id import MessageID
from terrex.packet.base import ServerPacket


class RequestPassword(ServerPacket):
    id = MessageID.RequestPassword

    def read(self, reader):
        pass
