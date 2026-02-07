from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds


class ClientSyncedInventory(ClientPacket):
    id = PacketIds.CLIENT_FINISHED_INVENTORY_CHANGES.value

    def write(self, writer):
        pass


ClientSyncedInventory.register()
