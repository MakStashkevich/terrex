from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class PlayerTeam(Packet):
    id = PacketIds.PLAYER_TEAM.value

    def __init__(self, player_id: int = 0, team: int = 0):
        self.player_id = player_id
        self.team = team

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.team = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.team)

PlayerTeam.register()