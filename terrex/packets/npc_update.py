from typing import List, Optional

from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader
from terrex.structures.vec2 import Vec2


class NpcUpdate(ServerPacket):
    id = PacketIds.NPC_UPDATE.value

    def __init__(self, npc_id: int = 0, pos: Vec2 = Vec2(0.0, 0.0), vel: Vec2 = Vec2(0.0, 0.0),
                 target: int = 0, flags: int = 0, ai: List[float] = None, npc_net_id: int = 0,
                 player_count_scale: Optional[int] = None, strength_multiplier: Optional[float] = None,
                 life: Optional[int] = None, release_owner: Optional[int] = None):
        self.npc_id = npc_id
        self.pos = pos
        self.vel = vel
        self.target = target
        self.flags = flags
        self.ai = ai or [0.0] * 4
        self.npc_net_id = npc_net_id
        self.player_count_scale = player_count_scale
        self.strength_multiplier = strength_multiplier
        self.life = life
        self.release_owner = release_owner

    def read(self, reader: Reader):
        self.npc_id = reader.read_short()
        self.pos = Vec2.read(reader)
        self.vel = Vec2.read(reader)
        self.target = reader.read_ushort()
        self.flags = reader.read_ushort()
        ai_flags = [0x0004, 0x0008, 0x0010, 0x0020]
        for i in range(4):
            if self.flags & ai_flags[i]:
                self.ai[i] = reader.read_float()
        self.npc_net_id = reader.read_short()
        if self.flags & 0x0100:  # SCALE_PLAYER_COUNT
            self.player_count_scale = reader.read_byte()
        if self.flags & 0x0400:  # MULTIPLY_STRENGTH
            self.strength_multiplier = reader.read_float()
        if not (self.flags & 0x0080):  # NO_LIFE
            size = reader.read_byte()
            if size == 1:
                self.life = reader.read_sbyte()
            elif size == 2:
                self.life = reader.read_short()
            elif size == 4:
                self.life = reader.read_int()
        # release_owner if catchable - simplified, assume read if npc_net_id >= 0 and catchable
        if self.npc_net_id >= 0:  # simplified catchable check
            self.release_owner = reader.read_byte()

NpcUpdate.register()