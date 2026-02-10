from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader


class UpdateShieldStrengths(ServerPacket):
    id = PacketIds.UPDATE_SHIELD_STRENGTHS

    def __init__(self, solar_tower: int = 0, vortex_tower: int = 0, nebula_tower: int = 0, stardust_tower: int = 0):
        self.solar_tower = solar_tower
        self.vortex_tower = vortex_tower
        self.nebula_tower = nebula_tower
        self.stardust_tower = stardust_tower

    def read(self, reader: Reader):
        self.solar_tower = reader.read_ushort()
        self.vortex_tower = reader.read_ushort()
        self.nebula_tower = reader.read_ushort()
        self.stardust_tower = reader.read_ushort()


UpdateShieldStrengths.register()
