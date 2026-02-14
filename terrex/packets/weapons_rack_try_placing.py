from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class WeaponsRackTryPlacing(ClientPacket):
    id = MessageID.WeaponsRackTryPlacing

    def __init__(self, x: int = 0, y: int = 0, net_id: int = 0, prefix: int = 0, stack: int = 0):
        self.x = x
        self.y = y
        self.net_id = net_id
        self.prefix = prefix
        self.stack = stack

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.net_id)
        writer.write_byte(self.prefix)
        writer.write_short(self.stack)



