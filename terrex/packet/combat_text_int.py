from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.rgb import Rgb
from terrex.net.vec2 import Vec2
from terrex.net.streamer import Reader


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
