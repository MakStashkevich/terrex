from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.localization.network_text import NetworkText
from terrex.net.streamer import Reader


class StatusTextSize(ServerPacket):
    id = MessageID.StatusTextSize

    def __init__(self, status_id: int = 0, text: NetworkText | None = None, flags: int = 0):
        self.status_id = status_id
        self.text = text or NetworkText()
        self.flags = flags

    def read(self, reader: Reader):
        self.status_id = reader.read_int()
        self.text = NetworkText.read(reader)
        self.flags = reader.read_byte()
