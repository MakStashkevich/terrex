from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class HealEffect(SyncPacket):
    id = PacketIds.HEAL_EFFECT

    def __init__(self, player_id: int = 0, heal_amount: int = 0):
        self.player_id = player_id
        self.heal_amount = heal_amount

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.heal_amount = reader.read_short()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.heal_amount)

HealEffect.register()