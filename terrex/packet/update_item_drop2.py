from terrex.packet.sync_item import SyncItem
from terrex.id import MessageID


class InstancedItem(SyncItem):
    id = MessageID.InstancedItem
    # repeats logic UpdateItemDrop
