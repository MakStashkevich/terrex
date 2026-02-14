from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class QuickStackChests(ClientPacket):
    id = MessageID.QuickStackChests

    def __init__(self, inventory_slot: int = 0):
        self.inventory_slot = inventory_slot

    def read(self, reader: Reader) -> None:
        self.inventory_slot = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.inventory_slot)
