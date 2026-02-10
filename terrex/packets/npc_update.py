from typing import List, Optional

from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader
from terrex.structures.vec2 import Vec2


class NpcUpdate(ServerPacket):
    id = PacketIds.NPC_UPDATE

    def __init__(self, npc_id: int = 0, pos: Vec2 = Vec2(0.0, 0.0), vel: Vec2 = Vec2(0.0, 0.0),
                 target: int = 0, ai: List[float] = None, npc_net_id: int = 0,
                 player_count_scale: Optional[int] = None, strength_multiplier: Optional[float] = None,
                 life: Optional[int] = None, release_owner: Optional[int] = None,
                 direction: int = -1, direction_y_positive: bool = False, sprite_direction: int = -1,
                 full_life: bool = True, stats_scaled_gt1: bool = False, spawned_from_statue: bool = False,
                 difficulty_flag: bool = False, spawn_needs_syncing: bool = False, shimmer_transparency_gt0: bool = False,
                 life_size: Optional[int] = None):
        self.npc_id = npc_id
        self.pos = pos
        self.vel = vel
        self.target = target
        self.ai = ai or [0.0] * 4
        self.npc_net_id = npc_net_id
        self.player_count_scale = player_count_scale
        self.strength_multiplier = strength_multiplier
        self.life = life
        self.release_owner = release_owner
        self.direction = direction
        self.direction_y_positive = direction_y_positive
        self.sprite_direction = sprite_direction
        self.full_life = full_life
        self.stats_scaled_gt1 = stats_scaled_gt1
        self.spawned_from_statue = spawned_from_statue
        self.difficulty_flag = difficulty_flag
        self.spawn_needs_syncing = spawn_needs_syncing
        self.shimmer_transparency_gt0 = shimmer_transparency_gt0
        self.life_size = life_size

    def read(self, reader: Reader):
        self.npc_id = reader.read_short()
        self.pos = Vec2.read(reader)
        self.vel = Vec2.read(reader)
        self.target = reader.read_ushort()
        bits1 = reader.read_byte()
        self.direction = 1 if (bits1 & 0x01) else -1
        self.direction_y_positive = bool(bits1 & 0x02)
        ai_active = [(bits1 & (0x04 << i)) != 0 for i in range(4)]
        self.sprite_direction = 1 if (bits1 & 0x40) else -1
        self.full_life = bool(bits1 & 0x80)
        bits2 = reader.read_byte()
        self.stats_scaled_gt1 = bool(bits2 & 0x01)
        self.spawned_from_statue = bool(bits2 & 0x02)
        self.difficulty_flag = bool(bits2 & 0x04)
        self.spawn_needs_syncing = bool(bits2 & 0x08)
        self.shimmer_transparency_gt0 = bool(bits2 & 0x10)
        self.ai = [0.0] * 4
        for i in range(4):
            if ai_active[i]:
                self.ai[i] = reader.read_float()
        self.npc_net_id = reader.read_short()
        self.player_count_scale = None
        if self.stats_scaled_gt1:
            self.player_count_scale = reader.read_byte()
        self.strength_multiplier = None
        if self.difficulty_flag:
            self.strength_multiplier = reader.read_float()
        self.life = None
        self.life_size = None
        if not self.full_life:
            self.life_size = reader.read_byte()
            size = self.life_size
            if size == 1:
                self.life = reader.read_sbyte()
            elif size == 2:
                self.life = reader.read_short()
            elif size == 4:
                self.life = reader.read_int()
        self.release_owner = None
        if not reader.eof():
            self.release_owner = reader.read_byte()

NpcUpdate.register()