from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class PlayerLifeMana(SyncPacket):
    id = MessageID.PlayerLifeMana

    def __init__(self, player_id: int = 0, hp: int = 100, max_hp: int = 100):
        self.player_id = player_id
        self.hp = hp
        self.max_hp = max_hp

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.hp = reader.read_ushort()
        self.max_hp = reader.read_ushort()

    async def handle(self, world, player, evman):
        if not self.player_id in world.players:
            return
        current_player = world.players[self.player_id]
        current_player.currHP = self.hp
        current_player.maxHP = self.max_hp

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_ushort(self.hp)
        writer.write_ushort(self.max_hp)
