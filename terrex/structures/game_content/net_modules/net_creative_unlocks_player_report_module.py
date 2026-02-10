from terrex.util.streamer import Reader, Writer
from .base import NetClientModule


class NetCreativeUnlocksPlayerReportModule(NetClientModule):
    def __init__(self, player_id: int, item_id: int, amount: int):
        self.player_id = player_id
        self.item_id = item_id
        self.amount = amount

    @classmethod
    def read(cls, reader: Reader) -> 'NetCreativeUnlocksPlayerReportModule':
        player_id = reader.read_byte()
        item_id = reader.read_ushort()
        amount = reader.read_ushort()
        return cls(player_id, item_id, amount)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_ushort(self.item_id)
        writer.write_ushort(self.amount)
