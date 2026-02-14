from terrex.structures.id import MessageID

from ..structures.vec2 import Vec2
from ..util.streamer import Reader, Writer
from .base import ClientPacket


class BugReleasing(ClientPacket):
    id = MessageID.BugReleasing

    def __init__(self) -> None:
        self.position: Vec2 = Vec2(0, 0)
        self.npc_type: int = 0
        self.style: int = 0

    def read(self, reader: Reader) -> None:
        self.position = Vec2(reader.read_int(), reader.read_int())
        self.npc_type = reader.read_short()
        self.style = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_int(int(self.position.x))
        writer.write_int(int(self.position.y))
        writer.write_short(self.npc_type)
        writer.write_byte(self.style)
