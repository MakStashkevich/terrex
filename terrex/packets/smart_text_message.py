from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader
from terrex.structures.net_string import NetString

class SmartTextMessage(ServerPacket):
    id = PacketIds.SMART_TEXT_MESSAGE.value

    def __init__(self, color_r: int = 255, color_g: int = 255, color_b: int = 255, message: NetString = NetString(), message_length: int = 0):
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.message = message
        self.message_length = message_length

    def read(self, reader: Reader) -> None:
        self.color_r = reader.read_byte()
        self.color_g = reader.read_byte()
        self.color_b = reader.read_byte()
        self.message = NetString.read(reader)
        self.message_length = reader.read_short()

    def handle(self, world, player, evman):
        pass

SmartTextMessage.register()