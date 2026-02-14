from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader
from terrex.structures.localization.network_text import NetworkText

class SmartTextMessage(ServerPacket):
    id = MessageID.SmartTextMessage

    def __init__(self, color_r: int = 255, color_g: int = 255, color_b: int = 255, message: NetworkText = NetworkText(), message_length: int = 0):
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.message = message
        self.message_length = message_length

    def read(self, reader: Reader) -> None:
        self.color_r = reader.read_byte()
        self.color_g = reader.read_byte()
        self.color_b = reader.read_byte()
        self.message = NetworkText.read(reader)
        self.message_length = reader.read_short()

    def handle(self, world, player, evman):
        pass

