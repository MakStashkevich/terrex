from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.structures.rgb import Rgb
from terrex.structures.vec2 import Vec2
from terrex.structures.localization.network_text import NetworkText
from terrex.util.streamer import Reader, Writer


class CombatTextString(SyncPacket):
    id = MessageID.CombatTextString

    def __init__(self, pos: Vec2 | None = None, color: Rgb | None = None, combat_text: NetworkText | None = None):
        self.pos = pos or Vec2(0.0, 0.0)
        self.color = color or Rgb(0, 0, 0)
        self.combat_text = combat_text or NetworkText()

    def read(self, reader: Reader):
        self.pos = Vec2.read(reader)
        self.color = Rgb.read(reader)
        self.combat_text = NetworkText.read(reader)

    def write(self, writer: Writer):
        self.pos.write(writer)
        self.color.write(writer)
        self.combat_text.write(writer)



