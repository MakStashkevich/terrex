from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID


class ClientSyncedInventory(ClientPacket):
    id = MessageID.ClientSyncedInventory

    def write(self, writer):
        pass
