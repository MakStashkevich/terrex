from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class RemoveItemOwner(Packet):
    id = PacketIds.REMOVE_ITEM_OWNER.value

    def __init__(self, item_index: int = 0):
        self.item_index = item_index

    def read(self, reader: Reader):
        self.item_index = reader.read_ushort()

    def write(self, writer: Writer):
        writer.write_ushort(self.item_index)

RemoveItemOwner.register()