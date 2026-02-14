from typing import Any

from terrex.packets.base import SyncPacket

from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


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

