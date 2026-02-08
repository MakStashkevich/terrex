from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class SyncTilePicking(SyncPacket):
    id = 125

    def __init__(self, player_id: int = 0, x: int = 0, y: int = 0, pick_damage: int = 0):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.pick_damage = pick_damage

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.pick_damage = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_byte(self.pick_damage)

    def handle(self, world, player, evman):
        pass

SyncTilePicking.register()