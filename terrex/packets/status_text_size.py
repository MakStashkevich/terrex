from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.structures.localization.network_text import NetworkText
from terrex.util.streamer import Reader


class StatusTextSize(ServerPacket):
    id = MessageID.StatusTextSize

    def __init__(self, status_id: int = 0, text: NetworkText = NetworkText(), flags: int = 0):
        self.status_id = status_id
        self.text = text
        self.flags = flags

    def read(self, reader: Reader):
        self.status_id = reader.read_int()
        self.text = NetworkText.read(reader)
        self.flags = reader.read_byte()
