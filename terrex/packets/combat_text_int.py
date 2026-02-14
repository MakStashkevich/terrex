from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.structures.rgb import Rgb
from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer


class CombatTextInt(ServerPacket):
    id = MessageID.CombatTextInt

    def __init__(self, pos: Vec2 | None = None, color: Rgb | None = None, heal_amount: int = 0):
        self.pos = pos or Vec2(0.0, 0.0)
        self.color = color or Rgb(0, 0, 0)
        self.heal_amount = heal_amount

    def read(self, reader: Reader):
        self.pos = Vec2.read(reader)
        self.color = Rgb.read(reader)
        self.heal_amount = reader.read_int()



