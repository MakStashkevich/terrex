from terrex.packets.base import Packet
from terrex.structures.id import MessageID


class Unknown67(Packet):
    # Placeholder for TShock
    id = MessageID.Unknown67

    def read(self, reader):
        pass

    def write(self, writer):
        pass
