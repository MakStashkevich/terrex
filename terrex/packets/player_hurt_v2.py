from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.structures.player_death_reason import PlayerDeathReason
from terrex.util.streamer import Reader, Writer


class PlayerHurtV2(ClientPacket):
    id = MessageID.PlayerHurtV2

    def __init__(
        self,
        player_id: int = 0,
        reason: PlayerDeathReason | None = None,
        damage: int = 0,
        hit_direction: int = 0,
        flags: int = 0,
        cooldown_counter: int = 0,
    ):
        self.player_id = player_id
        self.reason = reason or PlayerDeathReason()
        self.damage = damage
        self.hit_direction = hit_direction
        self.flags = flags
        self.cooldown_counter = cooldown_counter

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.reason = PlayerDeathReason.read(reader)
        self.damage = reader.read_short()
        self.hit_direction = reader.read_byte()
        self.flags = reader.read_byte()
        self.cooldown_counter = reader.read_sbyte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        self.reason.write(writer)
        writer.write_short(self.damage)
        writer.write_byte(self.hit_direction)
        writer.write_byte(self.flags)
        writer.write_sbyte(self.cooldown_counter)
