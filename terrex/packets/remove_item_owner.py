from typing import Any

from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class RemoveItemOwner(ServerPacket):
    id = PacketIds.REMOVE_ITEM_OWNER

    def read(self, reader: Reader):
        self.item_index = reader.read_ushort()

RemoveItemOwner.register()