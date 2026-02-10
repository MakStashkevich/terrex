from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class TogglePvp(SyncPacket):
    id = PacketIds.TOGGLE_PVP

    def __init__(self, player_id: int = 0, pvp_enabled: bool = False):
        self.player_id = player_id
        self.pvp_enabled = pvp_enabled

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.pvp_enabled = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_bool(self.pvp_enabled)

TogglePvp.register()