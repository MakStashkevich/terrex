from typing import Any

from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Writer


class OpenChest(ClientPacket):
    id = PacketIds.OPEN_CHEST.value

    def __init__(self, tile_x: int = 0, tile_y: int = 0):
        self.tile_x = tile_x
        self.tile_y = tile_y

    def write(self, writer: Writer):
        writer.write_short(self.tile_x)
        writer.write_short(self.tile_y)

OpenChest.register()