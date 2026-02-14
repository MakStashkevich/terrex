from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


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
