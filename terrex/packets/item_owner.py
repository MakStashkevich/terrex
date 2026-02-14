from typing import Any

from terrex.events.events import Event
from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class ItemOwner(SyncPacket):
    id = MessageID.ItemOwner

    def __init__(self, item_id: int = 0, player_id: int = 0):
        self.item_id = item_id
        self.player_id = player_id

    def read(self, reader: Reader):
        self.item_id = reader.read_short()
        self.player_id = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.item_id)
        writer.write_byte(self.player_id)
        
    def handle(self, world, player, evman):
        world.item_owner_index[self.item_id] = self.player_id
        evman.raise_event(Event.ItemOwnerChanged, (self.item_id, self.player_id))

