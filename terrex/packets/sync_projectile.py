from typing import List, Optional

from terrex.packets.base import SyncPacket

from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer
from terrex.structures.vec2 import Vec2


class SyncProjectile(SyncPacket):
    id = MessageID.SyncProjectile

    def __init__(self, projectile_id: int = 0, pos: Vec2 = Vec2(0.0, 0.0), vel: Vec2 = Vec2(0.0, 0.0),
                 owner: int = 0, ty: int = 0, flags: int = 0, ai: List[float] = None,
                 damage: Optional[int] = None, knockback: Optional[float] = None,
                 original_damage: Optional[int] = None, proj_uuid: Optional[int] = None):
        self.projectile_id = projectile_id
        self.pos = pos
        self.vel = vel
        self.owner = owner
        self.ty = ty
        self.flags = flags
        self.ai = ai or [0.0] * 2
        self.damage = damage
        self.knockback = knockback
        self.original_damage = original_damage
        self.proj_uuid = proj_uuid

    def read(self, reader: Reader):
        self.projectile_id = reader.read_short()
        self.pos = Vec2.read(reader)
        self.vel = Vec2.read(reader)
        self.owner = reader.read_byte()
        self.ty = reader.read_short()
        self.flags = reader.read_byte()
        ai_flags = [0x01, 0x02]
        for i in range(2):
            if self.flags & ai_flags[i]:
                self.ai[i] = reader.read_float()
        if self.flags & 0x10:  # HAS_DAMAGE
            self.damage = reader.read_short()
        if self.flags & 0x20:  # HAS_KNOCKBACK
            self.knockback = reader.read_float()
        if self.flags & 0x40:  # HAS_ORIG_DAMAGE
            self.original_damage = reader.read_short()
        if self.flags & 0x80:  # HAS_UUID
            self.proj_uuid = reader.read_short()

    def write(self, writer: Writer):
        writer.write_short(self.projectile_id)
        self.pos.write(writer)
        self.vel.write(writer)
        writer.write_byte(self.owner)
        writer.write_short(self.ty)
        writer.write_byte(self.flags)
        ai_flags = [0x01, 0x02]
        for i in range(2):
            if self.flags & ai_flags[i]:
                writer.write_float(self.ai[i])
        if self.damage is not None:
            writer.write_short(self.damage)
        if self.knockback is not None:
            writer.write_float(self.knockback)
        if self.original_damage is not None:
            writer.write_short(self.original_damage)
        if self.proj_uuid is not None:
            writer.write_short(self.proj_uuid)

