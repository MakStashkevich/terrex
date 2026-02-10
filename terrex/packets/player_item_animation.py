from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class PlayerItemAnimation(SyncPacket):
    id = PacketIds.PLAYER_ITEM_ANIMATION

    def __init__(self, player_id: int = 0, item_rotation: float = 0.0, item_animation: int = 0):
        self.player_id = player_id
        self.item_rotation = item_rotation
        self.item_animation = item_animation

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.item_rotation = reader.read_float()
        self.item_animation = reader.read_short()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_float(self.item_rotation)
        writer.write_short(self.item_animation)

PlayerItemAnimation.register()