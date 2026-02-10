from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Writer


class RequestNpcDebuff(ClientPacket):
    id = PacketIds.REQUEST_NPC_BUFF_REMOVAL

    def __init__(self, npc_id: int = 0, buff_id: int = 0):
        self.npc_id = npc_id
        self.buff_id = buff_id

    def write(self, writer: Writer):
        writer.write_short(self.npc_id)
        writer.write_ushort(self.buff_id)


RequestNpcDebuff.register()
