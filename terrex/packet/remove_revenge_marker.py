from terrex.id import MessageID
from terrex.net.streamer import Reader
from terrex.packet.base import ServerPacket


class RemoveRevengeMarker(ServerPacket):
    id = MessageID.RemoveRevengeMarker

    def __init__(self, unique_id: int = 0):
        self.unique_id = unique_id

    def read(self, reader: Reader) -> None:
        self.unique_id = reader.read_int()
