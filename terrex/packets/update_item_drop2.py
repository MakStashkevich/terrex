from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer
from terrex.structures.vec2 import Vec2


class UpdateItemDrop2(SyncPacket):
    id = PacketIds.UPDATE_ITEM_DROP_2.value

    def __init__(self, item_id: int = 0, pos: Vec2 = Vec2(0.0, 0.0), vel: Vec2 = Vec2(0.0, 0.0),
                 stack_size: int = 0, prefix: int = 0, no_delay: int = 0, item_net_id: int = 0):
        self.item_id = item_id
        self.pos = pos
        self.vel = vel
        self.stack_size = stack_size
        self.prefix = prefix
        self.no_delay = no_delay
        self.item_net_id = item_net_id

    def read(self, reader: Reader):
        self.item_id = reader.read_short()
        self.pos = Vec2.read(reader)
        self.vel = Vec2.read(reader)
        self.stack_size = reader.read_short()
        self.prefix = reader.read_byte()
        self.no_delay = reader.read_byte()
        self.item_net_id = reader.read_short()

    def write(self, writer: Writer):
        writer.write_short(self.item_id)
        self.pos.write(writer)
        self.vel.write(writer)
        writer.write_short(self.stack_size)
        writer.write_byte(self.prefix)
        writer.write_byte(self.no_delay)
        writer.write_short(self.item_net_id)

UpdateItemDrop2.register()