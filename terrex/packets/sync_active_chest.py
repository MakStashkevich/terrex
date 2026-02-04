from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class SyncActiveChest(SyncPacket):
    id = PacketIds.SYNC_ACTIVE_CHEST.value

    def __init__(self, chest_id: int = 0, x: int = 0, y: int = 0, name: str = ""):
        self.chest_id = chest_id
        self.x = x
        self.y = y
        self.name = name

    def read(self, reader: Reader):
        self.chest_id = reader.read_short()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.name = reader.read_string()

    def write(self, writer: Writer):
        writer.write_short(self.chest_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_string(self.name)

SyncActiveChest.register()