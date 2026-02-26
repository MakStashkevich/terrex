from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer

from .base import SyncPacket


class SpecialFX(SyncPacket):
    id = MessageID.SpecialFX

    def __init__(self) -> None:
        self.player_id: int = 0
        self.effect_type: int = (
            0  # 1=SpawnSkeletron, 2=SoundAtPlayer, 3=StartSundialing, 4=BigMimicSpawnSmoke, 5=RegisterTorchGodBestiary
        )

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.effect_type = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_byte(self.effect_type)
