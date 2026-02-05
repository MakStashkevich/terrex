from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class PlayerZone(SyncPacket):
    id = PacketIds.PLAYER_ZONE.value

    def __init__(self, player_id: int = 0, flags: int = 0):
        self.player_id = player_id
        self.flags = flags

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.flags = reader.read_int()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_int(self.flags)

PlayerZone.register()