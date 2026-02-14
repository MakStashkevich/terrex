from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class UpdatePlayerLuckFactors(SyncPacket):
    id = MessageID.UpdatePlayerLuckFactors

    # maximum luck: 1.0
    # minimum luck: -0.4
    def __init__(
        self,
        player_id: int = 0,
        ladybug_luck_time_left: int = 0,
        torch_luck: float = 0.0,
        luck_potion: int = 0,
        has_garden_gnome_nearby: bool = False,
        broken_mirror_bad_luck: bool = False,
        equipment_based_luck_bonus: float = 0.0,
        coin_luck: float = 0.0,
        kite_luck_level: int = 0,
    ):
        self.player_id = player_id
        self.ladybug_luck_time_left = ladybug_luck_time_left
        self.torch_luck = torch_luck
        self.luck_potion = luck_potion
        self.has_garden_gnome_nearby = has_garden_gnome_nearby
        self.broken_mirror_bad_luck = broken_mirror_bad_luck
        self.equipment_based_luck_bonus = equipment_based_luck_bonus
        self.coin_luck = coin_luck
        self.kite_luck_level = kite_luck_level

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.ladybug_luck_time_left = reader.read_int()
        self.torch_luck = reader.read_float()
        self.luck_potion = reader.read_byte()
        self.has_garden_gnome_nearby = reader.read_bool()
        self.broken_mirror_bad_luck = reader.read_bool()
        self.equipment_based_luck_bonus = reader.read_float()
        self.coin_luck = reader.read_float()
        self.kite_luck_level = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_int(self.ladybug_luck_time_left)
        writer.write_float(self.torch_luck)
        writer.write_byte(self.luck_potion)
        writer.write_bool(self.has_garden_gnome_nearby)
        writer.write_bool(self.broken_mirror_bad_luck)
        writer.write_float(self.equipment_based_luck_bonus)
        writer.write_float(self.coin_luck)
        writer.write_byte(self.kite_luck_level)



