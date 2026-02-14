from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class SyncPlayerZone(SyncPacket):
    id = MessageID.SyncPlayerZone

    def __init__(self, player_id: int = 0, flags: int = 0):
        self.player_id = player_id
        self.flags = flags

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.flags = reader.read_int()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_int(self.flags)
