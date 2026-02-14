from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class AddNPCBuff(SyncPacket):
    id = MessageID.AddNPCBuff

    def __init__(self, npc_id: int = 0, buff: int = 0, time: int = 0):
        self.npc_id = npc_id
        self.buff = buff
        self.time = time

    def read(self, reader: Reader):
        self.npc_id = reader.read_short()
        self.buff = reader.read_ushort()
        self.time = reader.read_short()

    def write(self, writer: Writer):
        writer.write_short(self.npc_id)
        writer.write_ushort(self.buff)
        writer.write_short(self.time)

 

