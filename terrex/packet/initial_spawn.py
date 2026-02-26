from terrex.id import MessageID
from terrex.packet.base import ServerPacket


class InitialSpawn(ServerPacket):
    id = MessageID.InitialSpawn

    def read(self, reader):
        pass
