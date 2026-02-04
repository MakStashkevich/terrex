from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class PlayerActive(Packet):
    id = PacketIds.PLAYER_ACTIVE.value

    def __init__(self, player_id: int = 0, active: bool = False):
        self.player_id = player_id
        self.active = active

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.active = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_bool(self.active)

PlayerActive.register()