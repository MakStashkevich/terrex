from typing import Any

from terrex.item.item import Item
from terrex.events.events import Event
from terrex.packets.sync_item import SyncItem
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer
from terrex.structures.vec2 import Vec2


class InstancedItem(SyncItem):
    id = MessageID.InstancedItem
    # repeats logic UpdateItemDrop

