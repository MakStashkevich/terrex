from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer
from terrex.structures.player_death_reason import PlayerDeathReason


class PlayerDeath(ClientPacket):
    id = PacketIds.PLAYER_DEATH_V2

    def __init__(
        self,
        player_id: int = 0,
        reason: PlayerDeathReason | None = None,
        damage: int = 0,
        hit_direction: int = 0,
        pvp: bool = False,
    ):
        self.player_id = player_id
        self.reason = reason or PlayerDeathReason()
        self.damage = damage
        self.hit_direction = hit_direction
        self.pvp = pvp

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.reason = PlayerDeathReason.read(reader)
        self.damage = reader.read_short()
        self.hit_direction = reader.read_byte()
        self.pvp = reader.read_bool()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        self.reason.write(writer)
        writer.write_short(self.damage)
        writer.write_byte(self.hit_direction)
        writer.write_bool(self.pvp)


PlayerDeath.register()
