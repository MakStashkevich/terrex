from dataclasses import dataclass
from terrex.util.streamer import Reader, Writer
from .net_module import NetServerModule


@dataclass()
class NetUnbreakableWallScanModule(NetServerModule):
    id: int = 14
    player_id: int | None = None
    inside_unbreakable_walls: bool | None = None

    @classmethod
    def create(cls, player_id: int, inside_unbreakable_walls: bool) -> "NetUnbreakableWallScanModule":
        obj = cls()
        obj.player_id = player_id
        obj.inside_unbreakable_walls = inside_unbreakable_walls
        return obj

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.inside_unbreakable_walls = reader.read_bool()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_bool(self.inside_unbreakable_walls)
