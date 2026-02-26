from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer

from .net_module import NetClientModule


@dataclass()
class NetCreativeUnlocksPlayerReportModule(NetClientModule):
    id: int = 6
    player_id: int | None = None
    item_id: int | None = None
    amount: int = 0

    @classmethod
    def create(
        cls, player_id: int, item_id: int, amount: int = 0
    ) -> "NetCreativeUnlocksPlayerReportModule":
        obj = cls()
        obj.player_id = player_id
        obj.item_id = item_id
        obj.amount = amount
        return obj

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.item_id = reader.read_ushort()
        self.amount = reader.read_ushort()

    def write(self, writer: Writer) -> None:
        if self.player_id is None or self.item_id is None:
            raise ValueError("player_id and item_id must not be None")
        writer.write_byte(self.player_id)
        writer.write_ushort(self.item_id)
        writer.write_ushort(self.amount)
