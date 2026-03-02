from terrex.event.context import EventHandleContext
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class TogglePvp(SyncPacket):
    id = MessageID.TogglePVP

    def __init__(self, player_id: int = 0, pvp_enabled: bool = False):
        self.player_id = player_id
        self.pvp_enabled = pvp_enabled

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.pvp_enabled = reader.read_bool()
        
    async def handle(self, ctx: EventHandleContext):
        if not self.player_id in ctx.world.players:
            return
        current_player = ctx.world.players[self.player_id]
        current_player.pvp_enabled = self.pvp_enabled

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_bool(self.pvp_enabled)
