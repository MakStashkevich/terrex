from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer


class SyncExtraValue(SyncPacket):
    id = MessageID.SyncExtraValue

    def __init__(self, npc_index: int = 0, extra_value: int = 0, pos: Vec2 | None = None):
        self.npc_index = npc_index
        self.extra_value = extra_value
        self.pos = pos or Vec2(0.0, 0.0)

    def read(self, reader: Reader):
        self.npc_index = reader.read_ushort()
        self.extra_value = reader.read_int()
        self.pos = Vec2.read(reader)

    def write(self, writer: Writer):
        writer.write_ushort(self.npc_index)
        writer.write_int(self.extra_value)
        self.pos.write(writer)



