from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class ReleaseItemOwnership(ServerPacket):
    id = MessageID.ReleaseItemOwnership

    def read(self, reader: Reader):
        self.item_index = reader.read_ushort()
