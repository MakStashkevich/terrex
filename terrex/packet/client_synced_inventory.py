from terrex.packet.base import ClientPacket
from terrex.id import MessageID


class ClientSyncedInventory(ClientPacket):
    id = MessageID.ClientSyncedInventory

    def write(self, writer):
        pass
