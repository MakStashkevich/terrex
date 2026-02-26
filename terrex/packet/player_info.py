from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class PlayerInfo(ServerPacket):
    id = MessageID.PlayerInfo

    def __init__(self, player_id: int = 0, is_server: bool = False):
        self.player_id = player_id
        self.is_server = is_server

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.is_server = reader.read_bool()
