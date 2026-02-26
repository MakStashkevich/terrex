from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer

from .base import ClientPacket


class SpawnBossUseLicenseStartEvent(ClientPacket):
    id = MessageID.SpawnBossUseLicenseStartEvent

    def __init__(self) -> None:
        self.player_id: int = 0
        self.invasion_type: int = 0  # positive for bosses, negative for invasions

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_short()
        self.invasion_type = reader.read_short()

    def write(self, writer: Writer) -> None:
        writer.write_short(self.player_id)
        writer.write_short(self.invasion_type)
