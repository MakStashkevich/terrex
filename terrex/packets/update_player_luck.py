from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class UpdatePlayerLuck(SyncPacket):
    id = PacketIds.UPDATE_PLAYER_LUCK_FACTORS.value

    # maximum luck: 1.0
    # minimum luck: -0.4
    def __init__(self,
                 player_id: int = 0,
                 ladybug_luck_time_remaining: int = 0,
                 torch_luck: float = 0.0,
                 luck_potion: int = 0,
                 has_garden_gnome_nearby: bool = False):
        self.player_id = player_id
        self.ladybug_luck_time_remaining = ladybug_luck_time_remaining # +0.2-0.4 (if ladubug is golden) (time 12-24 min)
        self.torch_luck = torch_luck # +0.2 (+0.1 if torch primary)
        self.luck_potion = luck_potion # +0.1 - 0.2 - 0.3 (5 - 10 - 15 min)
        self.has_garden_gnome_nearby = has_garden_gnome_nearby # +0.2
        
        # счастливая монета +0.05
        # подкова +0.05

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.ladybug_luck_time_remaining = reader.read_int()
        self.torch_luck = reader.read_float()
        self.luck_potion = reader.read_byte()
        self.has_garden_gnome_nearby = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_int(self.ladybug_luck_time_remaining)
        writer.write_float(self.torch_luck)
        writer.write_byte(self.luck_potion)
        writer.write_bool(self.has_garden_gnome_nearby)


UpdatePlayerLuck.register()
