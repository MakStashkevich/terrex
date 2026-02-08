from terrex.packets.packet_ids import PacketIds
from terrex.packets.base import ClientPacket
from terrex.util.streamer import Reader, Writer


class ForceItemNearestChest(ClientPacket):
    id = PacketIds.FORCE_ITEM_NEAREST_CHEST.value

    def __init__(self, inventory_slot: int = 0):
        self.inventory_slot = inventory_slot

    def read(self, reader: Reader) -> None:
        self.inventory_slot = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.inventory_slot)

ForceItemNearestChest.register()