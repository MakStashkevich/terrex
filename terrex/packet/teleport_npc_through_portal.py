from terrex.packet.base import SyncPacket
from terrex.id import MessageID
from terrex.net.structure.vec2 import Vec2
from terrex.net.streamer import Reader, Writer


class TeleportNPCThroughPortal(SyncPacket):
    id = MessageID.TeleportNPCThroughPortal

    def __init__(self, npc_id: int = 0, portal_color_index: int = 0, pos: Vec2 | None = None, vel: Vec2 | None = None):
        self.npc_id = npc_id
        self.portal_color_index = portal_color_index
        self.pos = pos or Vec2(0.0, 0.0)
        self.vel = vel or Vec2(0.0, 0.0)

    def read(self, reader: Reader):
        self.npc_id = reader.read_ushort()
        self.portal_color_index = reader.read_ushort()
        self.pos = Vec2.read(reader)
        self.vel = Vec2.read(reader)

    def write(self, writer: Writer):
        writer.write_ushort(self.npc_id)
        writer.write_ushort(self.portal_color_index)
        self.pos.write(writer)
        self.vel.write(writer)
