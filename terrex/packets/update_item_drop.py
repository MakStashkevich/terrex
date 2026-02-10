from typing import Any

from terrex.data.item import Item
from terrex.events.events import Event
from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.packets.update_item_drop2 import UpdateItemDrop2
from terrex.util.streamer import Reader, Writer
from terrex.structures.vec2 import Vec2


class UpdateItemDrop(SyncPacket):
    id = PacketIds.UPDATE_ITEM_DROP.value

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
        
    def handle(self, world, player, evman):
        # todo: fix Item props
        item_object = Item(self.item_id, self.item_net_id, self.pos, self.vel, self.prefix, self.stack_size)

        if self.item_id in world.items:
            evman.raise_event(Event.ItemDropUpdate, item_object)
        else:
            world.items[self.item_id] = item_object
            if not self.item_id in world.item_owner_index:
                world.item_owner_index[self.item_id] = 255
            evman.raise_event(Event.ItemDropped, item_object)

UpdateItemDrop.register()