from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class HealOtherPlayer(SyncPacket):
    id = MessageID.HealOtherPlayer

    def __init__(self, player_id: int = 0, heal_amount: int = 0):
        self.player_id = player_id
        self.heal_amount = heal_amount

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.heal_amount = reader.read_short()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.heal_amount)
