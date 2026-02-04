from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class ManaEffect(SyncPacket):
    id = PacketIds.MANA_EFFECT.value

    def __init__(self, player_id: int = 0, mana_amount: int = 0):
        self.player_id = player_id
        self.mana_amount = mana_amount

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.mana_amount = reader.read_short()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.mana_amount)

ManaEffect.register()