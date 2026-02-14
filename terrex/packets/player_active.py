from typing import Any

 

from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader

 

class PlayerActive(ServerPacket):
    id = MessageID.PlayerActive

    def __init__(self, player_id: int = 0, active: bool = False):
        self.player_id = player_id
        self.active = active

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.active = reader.read_bool()

