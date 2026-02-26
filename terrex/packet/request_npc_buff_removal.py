from terrex.id import MessageID
from terrex.net.streamer import Writer
from terrex.packet.base import ClientPacket


class RequestNPCBuffRemoval(ClientPacket):
    id = MessageID.RequestNPCBuffRemoval

    def __init__(self, npc_id: int = 0, buff_id: int = 0):
        self.npc_id = npc_id
        self.buff_id = buff_id

    def write(self, writer: Writer):
        writer.write_short(self.npc_id)
        writer.write_ushort(self.buff_id)
