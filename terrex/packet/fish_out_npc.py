from terrex.id import MessageID
from terrex.net.streamer import Writer
from terrex.packet.base import ClientPacket


class FishOutNpc(ClientPacket):
    id = MessageID.FishOutNPC

    def __init__(self, x: int = 0, y: int = 0, npc_id: int = 0):
        self.x = x
        self.y = y
        self.npc_id = npc_id

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.npc_id)
