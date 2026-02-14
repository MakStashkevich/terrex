from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class ShopOverride(ServerPacket):
    id = MessageID.ShopOverride

    def __init__(self, slot: int = 0, item_type: int = 0, stack: int = 0, prefix: int = 0, value: int = 0, buy_once: bool = False):
        self.slot = slot
        self.item_type = item_type
        self.stack = stack
        self.prefix = prefix
        self.value = value
        self.buy_once = buy_once

    def read(self, reader: Reader):
        self.slot = reader.read_byte()
        self.item_type = reader.read_short()
        self.stack = reader.read_short()
        self.prefix = reader.read_byte()
        self.value = reader.read_int()
        self.buy_once = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_byte(self.slot)
        writer.write_short(self.item_type)
        writer.write_short(self.stack)
        writer.write_byte(self.prefix)
        writer.write_int(self.value)
        writer.write_bool(self.buy_once)



