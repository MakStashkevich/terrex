from .packet_ids import PacketIds
from .base import ClientPacket
from ..util.streamer import Reader, Writer


class SpawnBossInvasion(ClientPacket):
    id = PacketIds.SPAWN_BOSS_INVASION.value

    def __init__(self) -> None:
        self.player_id: int = 0
        self.invasion_type: int = 0  # positive for bosses, negative for invasions

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_short()
        self.invasion_type = reader.read_short()

    def write(self, writer: Writer) -> None:
        writer.write_short(self.player_id)
        writer.write_short(self.invasion_type)

SpawnBossInvasion.register()