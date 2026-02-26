from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class UnusedMeleeStrike(SyncPacket):
    id = MessageID.UnusedMeleeStrike

    def __init__(self, npc_id: int = 0, player_id: int = 0):
        self.npc_id = npc_id
        self.player_id = player_id

    def read(self, reader: Reader):
        self.npc_id = reader.read_short()
        self.player_id = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.npc_id)
        writer.write_byte(self.player_id)
