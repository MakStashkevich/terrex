from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class DamageNPC(SyncPacket):
    id = MessageID.DamageNPC

    def __init__(
        self,
        npc_id: int = 0,
        damage: int = 0,
        knockback: float = 0.0,
        hit_direction: int = 0,
        crit: bool = False,
    ):
        self.npc_id = npc_id
        self.damage = damage
        self.knockback = knockback
        self.hit_direction = hit_direction
        self.crit = crit

    def read(self, reader: Reader):
        self.npc_id = reader.read_short()
        self.damage = reader.read_short()
        self.knockback = reader.read_float()
        self.hit_direction = reader.read_byte()
        self.crit = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_short(self.npc_id)
        writer.write_short(self.damage)
        writer.write_float(self.knockback)
        writer.write_byte(self.hit_direction)
        writer.write_bool(self.crit)
