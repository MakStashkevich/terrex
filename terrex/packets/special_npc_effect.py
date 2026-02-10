from .packet_ids import PacketIds
from .base import SyncPacket
from ..util.streamer import Reader, Writer


class SpecialNpcEffect(SyncPacket):
    id = PacketIds.SPECIAL_NPC_EFFECT

    def __init__(self) -> None:
        self.player_id: int = 0
        self.effect_type: int = 0  # 1=SpawnSkeletron, 2=SoundAtPlayer, 3=StartSundialing, 4=BigMimicSpawnSmoke, 5=RegisterTorchGodBestiary

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.effect_type = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_byte(self.effect_type)

SpecialNpcEffect.register()