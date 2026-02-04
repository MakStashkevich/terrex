from typing import List
from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class UpdatePlayerBuff(SyncPacket):
    id = PacketIds.UPDATE_PLAYER_BUFF.value

    def __init__(self, player_id: int = 0, buffs: List[int] = None):
        self.player_id = player_id
        self.buffs = buffs or [0] * 22

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.buffs = [reader.read_ushort() for _ in range(22)]

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        for b in self.buffs:
            writer.write_ushort(b)

UpdatePlayerBuff.register()