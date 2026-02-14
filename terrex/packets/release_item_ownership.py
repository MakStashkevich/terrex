from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader


class ReleaseItemOwnership(ServerPacket):
    id = MessageID.ReleaseItemOwnership

    def read(self, reader: Reader):
        self.item_index = reader.read_ushort()
