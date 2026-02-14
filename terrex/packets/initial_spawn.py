from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID


class InitialSpawn(ServerPacket):
    id = MessageID.InitialSpawn

    def read(self, reader):
        pass
