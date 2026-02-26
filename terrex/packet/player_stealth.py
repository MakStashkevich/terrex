from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class PlayerStealth(SyncPacket):
    id = MessageID.PlayerStealth

    def __init__(self, player: int = 0, stealth: float = 0.0):
        self.player = player
        self.stealth = stealth

    def read(self, reader: Reader):
        self.player = reader.read_byte()
        self.stealth = reader.read_float()

    def write(self, writer: Writer):
        writer.write_byte(self.player)
        writer.write_float(self.stealth)
