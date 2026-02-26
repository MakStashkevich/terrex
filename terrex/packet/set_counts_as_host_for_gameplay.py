from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class SetCountsAsHostForGameplay(ServerPacket):
    id = MessageID.SetCountsAsHostForGameplay

    def __init__(self, player_id: int = 0, host: bool = False):
        self.player_id = player_id
        self.host = host

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.host = reader.read_bool()
