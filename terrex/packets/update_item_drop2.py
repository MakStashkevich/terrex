from terrex.packets.sync_item import SyncItem
from terrex.structures.id import MessageID


class InstancedItem(SyncItem):
    id = MessageID.InstancedItem
    # repeats logic UpdateItemDrop
