from typing import Any

from terrex.data.item import Item
from terrex.events.events import Event
from terrex.packets.packet_ids import PacketIds
from terrex.packets.update_item_drop import UpdateItemDrop
from terrex.util.streamer import Reader, Writer
from terrex.structures.vec2 import Vec2


class UpdateItemDrop2(UpdateItemDrop):
    id = PacketIds.UPDATE_ITEM_DROP_2
    # repeats logic UpdateItemDrop

UpdateItemDrop2.register()