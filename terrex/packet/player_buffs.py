from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class PlayerBuffs(SyncPacket):
    id = MessageID.PlayerBuffs
    MAX_BUFF = 44  # Player.maxBuffs

    def __init__(self, player_id: int = 0, buffs: list[int] | None = None):
        self.player_id = player_id
        self.buffs: list[int] = buffs or []

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.buffs = []
        while len(self.buffs) < self.MAX_BUFF:
            buff = reader.read_ushort()
            if buff == 0:  # packet every end on 0 ushort
                break  # packet ended
            self.buffs.append(buff)

    async def handle(self, world, player, evman):
        if not self.player_id in world.players:
            return
        current_player = world.players[self.player_id]
        current_player.buffs = self.buffs

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        for b in self.buffs:
            writer.write_ushort(b)
        writer.write_ushort(0)
