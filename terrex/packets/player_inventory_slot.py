from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class PlayerInventorySlot(SyncPacket):
    id = PacketIds.PLAYER_INVENTORY_SLOT.value

    def __init__(self, player_id: int = 0, slot_id: int = 0, stack: int = 0, prefix: int = 0, item_netid: int = 0):
        self.player_id = player_id
        self.slot_id = slot_id
        self.stack = stack
        self.prefix = prefix
        self.item_netid = item_netid

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.slot_id = reader.read_short()
        self.stack = reader.read_short()
        self.prefix = reader.read_byte()
        self.item_netid = reader.read_ushort()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.slot_id)
        writer.write_short(self.stack)
        writer.write_byte(self.prefix)
        writer.write_ushort(self.item_netid)

PlayerInventorySlot.register()