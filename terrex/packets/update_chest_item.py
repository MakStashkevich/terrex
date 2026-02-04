from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class UpdateChestItem(Packet):
    id = PacketIds.UPDATE_CHEST_ITEM.value

    def __init__(self, chest_id: int = 0, item_slot: int = 0, stack: int = 0, prefix: int = 0, item_net_id: int = 0):
        self.chest_id = chest_id
        self.item_slot = item_slot
        self.stack = stack
        self.prefix = prefix
        self.item_net_id = item_net_id

    def read(self, reader: Reader):
        self.chest_id = reader.read_short()
        self.item_slot = reader.read_byte()
        self.stack = reader.read_short()
        self.prefix = reader.read_byte()
        self.item_net_id = reader.read_short()

    def write(self, writer: Writer):
        writer.write_short(self.chest_id)
        writer.write_byte(self.item_slot)
        writer.write_short(self.stack)
        writer.write_byte(self.prefix)
        writer.write_short(self.item_net_id)

UpdateChestItem.register()