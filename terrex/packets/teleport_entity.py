from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer


class TeleportEntity(SyncPacket):
    id = MessageID.TeleportEntity

    def __init__(self) -> None:
        self.flags: int = 0
        self.target_id: int = 0
        self.position: Vec2 = Vec2(0, 0)
        self.style: int = 0
        self.extra_info: int = 0

    def read(self, reader: Reader) -> None:
        self.flags = reader.read_byte()
        self.target_id = reader.read_short()
        self.position.x = reader.read_float()
        self.position.y = reader.read_float()
        self.style = reader.read_byte()
        if self.flags & 0x08:
            self.extra_info = reader.read_int()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.flags)
        writer.write_short(self.target_id)
        writer.write_float(self.position.x)
        writer.write_float(self.position.y)
        writer.write_byte(self.style)
        if self.flags & 0x08:
            writer.write_int(self.extra_info)
