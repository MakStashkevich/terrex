from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer

from .base import ServerPacket


class SyncPlayerChestIndex(ServerPacket):
    id = MessageID.SyncPlayerChestIndex

    def __init__(self) -> None:
        self.player_id: int = 0
        self.chest_id: int = 0

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.chest_id = reader.read_short()
        
    async def handle(self, world, player, evman):
        if not self.player_id in world.players:
            return
        current_player = world.players[self.player_id]
        current_player.chest_id = self.chest_id

    def write(self, writer: Writer) -> None:
        raise NotImplementedError(
            "Server does not send SyncPlayerChestIndex (client-bound packet only)"
        )
