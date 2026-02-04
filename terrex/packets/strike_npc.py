from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class StrikeNpc(SyncPacket):
    id = PacketIds.STRIKE_NPC_HELD_ITEM.value

    def __init__(self, npc_id: int = 0, player_id: int = 0):
        self.npc_id = npc_id
        self.player_id = player_id

    def read(self, reader: Reader):
        self.npc_id = reader.read_short()
        self.player_id = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.npc_id)
        writer.write_byte(self.player_id)

StrikeNpc.register()