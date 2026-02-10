from typing import List
from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class UpdatePlayerBuff(SyncPacket):
    id = PacketIds.UPDATE_PLAYER_BUFF.value
    MAX_BUFF = 44 # Player.maxBuffs

    def __init__(self, player_id: int = 0, buffs: List[int] = None):
        self.player_id = player_id
        self.buffs = buffs or []

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.buffs = []
        while len(self.buffs) < self.MAX_BUFF:
            buff = reader.read_ushort()
            if buff == 0: # packet every end on 0 ushort
                break # packet ended
            self.buffs.append(buff)

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        for b in self.buffs:
            writer.write_ushort(b)
        writer.write_ushort(0)

UpdatePlayerBuff.register()