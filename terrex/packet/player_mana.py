from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class PlayerMana(SyncPacket):
    id = MessageID.PlayerMana

    def __init__(self, player_id: int = 0, mana: int = 0, max_mana: int = 0):
        self.player_id = player_id
        self.mana = mana
        self.max_mana = max_mana

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.mana = reader.read_short()
        self.max_mana = reader.read_short()

    async def handle(self, world, player, evman):
        if not self.player_id in world.players:
            return
        current_player = world.players[self.player_id]
        current_player.currMana = self.mana
        current_player.maxMana = self.max_mana

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.mana)
        writer.write_short(self.max_mana)
