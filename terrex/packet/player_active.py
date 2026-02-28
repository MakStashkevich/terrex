from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class PlayerActive(ServerPacket):
    id = MessageID.PlayerActive

    def __init__(self, player_id: int = 0, active: bool = False):
        self.player_id = player_id
        self.active = active

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.active = reader.read_bool()

    async def handle(self, world, player, evman):
        if not self.active:
            return

        from terrex.player import Player

        world.players[self.player_id] = Player(world)
