from terrex.structures.id import MessageID
from .base import ServerPacket
from ..util.streamer import Reader, Writer


class SyncPlayerChestIndex(ServerPacket):
    id = MessageID.SyncPlayerChestIndex

    def __init__(self) -> None:
        self.player_id: int = 0
        self.chest_id: int = 0

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.chest_id = reader.read_short()

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Server does not send SyncPlayerChestIndex (client-bound packet only)")

