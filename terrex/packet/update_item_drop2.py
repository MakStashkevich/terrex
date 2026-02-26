from terrex.id import MessageID
from terrex.packet.sync_item import SyncItem


class InstancedItem(SyncItem):
    id = MessageID.InstancedItem
    # repeats logic UpdateItemDrop
