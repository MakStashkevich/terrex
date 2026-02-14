from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.structures.localization.network_text import NetworkText
from terrex.structures.rgb import Rgb
from terrex.util.streamer import Reader


class SmartTextMessage(ServerPacket):
    id = MessageID.SmartTextMessage

    def __init__(self, color: Rgb | None = None, message: NetworkText | None = None, message_length: int = 0):
        self.color = color
        self.message = message or NetworkText()
        self.message_length = message_length

    def read(self, reader: Reader) -> None:
        self.color = Rgb.read(reader)
        self.message = NetworkText.read(reader)
        self.message_length = reader.read_short()

    def handle(self, world, player, evman):
        pass
