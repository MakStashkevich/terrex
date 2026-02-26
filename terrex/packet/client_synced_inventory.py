from terrex.id import MessageID
from terrex.packet.base import ClientPacket


class ClientSyncedInventory(ClientPacket):
    id = MessageID.ClientSyncedInventory

    def write(self, writer):
        pass
