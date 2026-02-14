from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class AddPlayerBuffPvP(SyncPacket):
    id = MessageID.AddPlayerBuffPvP

    def __init__(self, player_id: int = 0, buff: int = 0, time: int = 0):
        self.player_id = player_id
        self.buff = buff
        self.time = time

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.buff = reader.read_ushort()
        self.time = reader.read_int()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_ushort(self.buff)
        writer.write_int(self.time)

 

