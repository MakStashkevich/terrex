from terrex.structures.id import MessageID
from terrex.packets.base import ServerPacket
from terrex.util.streamer import Reader, Writer


class ItemTweaker(ServerPacket):
    id = MessageID.ItemTweaker

    def __init__(self):
        self.item_index: int = 0
        self.flags1: int = 0
        self.packed_color: int = 0
        self.damage: int = 0
        self.knockback: float = 0.0
        self.use_animation: int = 0
        self.use_time: int = 0
        self.shoot: int = 0
        self.shoot_speed: float = 0.0
        self.flags2: int = 0
        self.width: int = 0
        self.height: int = 0
        self.scale: float = 0.0
        self.ammo: int = 0
        self.use_ammo: int = 0
        self.not_ammo: bool = False

    def read(self, reader: Reader) -> None:
        self.item_index = reader.read_short()
        self.flags1 = reader.read_byte()
        if self.flags1 & 1:
            self.packed_color = reader.read_int()
        if self.flags1 & 2:
            self.damage = reader.read_ushort()
        if self.flags1 & 4:
            self.knockback = reader.read_float()
        if self.flags1 & 8:
            self.use_animation = reader.read_ushort()
        if self.flags1 & 16:
            self.use_time = reader.read_ushort()
        if self.flags1 & 32:
            self.shoot = reader.read_short()
        if self.flags1 & 64:
            self.shoot_speed = reader.read_float()
        if self.flags1 & 128:
            self.flags2 = reader.read_byte()
            if self.flags2 & 1:
                self.width = reader.read_short()
            if self.flags2 & 2:
                self.height = reader.read_short()
            if self.flags2 & 4:
                self.scale = reader.read_float()
            if self.flags2 & 8:
                self.ammo = reader.read_short()
            if self.flags2 & 16:
                self.use_ammo = reader.read_short()
            if self.flags2 & 32:
                self.not_ammo = reader.read_bool()

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Server does not send TweakItem (client-bound packet only)")

