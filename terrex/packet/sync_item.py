from terrex.event.types import ItemDropUpdateEvent, ItemDroppedEvent
from terrex.item.item import Item
from terrex.packet.base import SyncPacket
from terrex.id import MessageID
from terrex.net.structure.vec2 import Vec2
from terrex.net.streamer import Reader, Writer


class SyncItem(SyncPacket):
    id = MessageID.SyncItem

    def __init__(self, item_id: int = 0, pos: Vec2 | None = None, vel: Vec2 | None = None, stack_size: int = 0, prefix: int = 0, no_delay: int = 0, item_net_id: int = 0):
        self.item_id = item_id
        self.pos = pos or Vec2(0.0, 0.0)
        self.vel = vel or Vec2(0.0, 0.0)
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

    async def handle(self, world, player, evman):
        # todo: fix Item props
        item = Item(self.item_id, self.item_net_id, self.pos, self.vel, self.prefix, self.stack_size)

        if self.item_id in world.items:
            evman.raise_event(ItemDropUpdateEvent(self, item))
        else:
            world.items[self.item_id] = item
            if self.item_id not in world.item_owner_index:
                world.item_owner_index[self.item_id] = 255
            evman.raise_event(ItemDroppedEvent(self, item))
