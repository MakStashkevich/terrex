from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader

class WiredCannonShot(ServerPacket):
    id = 108

    def __init__(self, damage: int = 0, knockback: float = 0.0, x: int = 0, y: int = 0, angle: int = 0, ammo: int = 0, player_id: int = 0):
        self.damage = damage
        self.knockback = knockback
        self.x = x
        self.y = y
        self.angle = angle
        self.ammo = ammo
        self.player_id = player_id

    def read(self, reader: Reader) -> None:
        self.damage = reader.read_short()
        self.knockback = reader.read_float()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.angle = reader.read_short()
        self.ammo = reader.read_short()
        self.player_id = reader.read_byte()

    def handle(self, world, player, evman):
        pass

WiredCannonShot.register()