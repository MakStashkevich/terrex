from terrex.event.context import EventHandleContext
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class TeamChange(SyncPacket):
    id = MessageID.TeamChange

    def __init__(self, player_id: int = 0, team: int = 0):
        self.player_id = player_id
        self.team = team

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.team = reader.read_byte()
        
    async def handle(self, ctx: EventHandleContext):
        if not self.player_id in ctx.world.players:
            return
        current_player = ctx.world.players[self.player_id]
        current_player.team = self.team

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.team)
