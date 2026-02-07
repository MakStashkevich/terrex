from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer


class NebulaLevelUp(SyncPacket):
    id = PacketIds.NEBULA_LEVEL_UP.value

    def __init__(self, player_id: int = 0, level_up_type: int = 0, origin: Vec2 | None = None):
        self.player_id = player_id
        self.level_up_type = level_up_type
        self.origin = origin or Vec2(0.0, 0.0)

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.level_up_type = reader.read_ushort()
        self.origin = Vec2.read(reader)

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_ushort(self.level_up_type)
        self.origin.write(writer)


NebulaLevelUp.register()
