from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class UpdateItemOwner(SyncPacket):
    id = PacketIds.UPDATE_ITEM_OWNER.value

    def __init__(self, item_id: int = 0, player_id: int = 0):
        self.item_id = item_id
        self.player_id = player_id

    def read(self, reader: Reader):
        self.item_id = reader.read_short()
        self.player_id = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.item_id)
        writer.write_byte(self.player_id)

UpdateItemOwner.register()