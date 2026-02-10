from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.structures.rgb import Rgb
from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer


class CreateCombatText(ServerPacket):
    id = PacketIds.CREATE_COMBAT_TEXT

    def __init__(self, pos: Vec2 | None = None, color: Rgb | None = None, heal_amount: int = 0):
        self.pos = pos or Vec2(0.0, 0.0)
        self.color = color or Rgb(0, 0, 0)
        self.heal_amount = heal_amount

    def read(self, reader: Reader):
        self.pos = Vec2.read(reader)
        self.color = Rgb.read(reader)
        self.heal_amount = reader.read_int()


CreateCombatText.register()
