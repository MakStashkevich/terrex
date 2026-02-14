from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class FoodPlatterTryPlacing(ClientPacket):
    id = MessageID.FoodPlatterTryPlacing

    def __init__(self, x: int = 0, y: int = 0, item_id: int = 0, prefix: int = 0, stack: int = 0):
        self.x = x
        self.y = y
        self.item_id = item_id
        self.prefix = prefix
        self.stack = stack

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.item_id)
        writer.write_byte(self.prefix)
        writer.write_short(self.stack)



