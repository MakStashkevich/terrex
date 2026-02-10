from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class PlayerMana(SyncPacket):
    id = PacketIds.PLAYER_MANA

    def __init__(self, player_id: int = 0, mana: int = 0, max_mana: int = 0):
        self.player_id = player_id
        self.mana = mana
        self.max_mana = max_mana

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.mana = reader.read_short()
        self.max_mana = reader.read_short()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.mana)
        writer.write_short(self.max_mana)

PlayerMana.register()