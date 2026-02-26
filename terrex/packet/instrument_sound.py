from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class InstrumentSound(SyncPacket):
    id = MessageID.InstrumentSound

    def __init__(self, player_id: int = 0, note: float = 0.0):
        self.player_id = player_id
        self.note = note

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.note = reader.read_float()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_float(self.note)
