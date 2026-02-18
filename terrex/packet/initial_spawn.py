from terrex.packet.base import ServerPacket
from terrex.id import MessageID


class InitialSpawn(ServerPacket):
    id = MessageID.InitialSpawn

    def read(self, reader):
        pass
