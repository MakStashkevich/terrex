from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class TeamChange(SyncPacket):
    id = MessageID.TeamChange

    def __init__(self, player_id: int = 0, team: int = 0):
        self.player_id = player_id
        self.team = team

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.team = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.team)
