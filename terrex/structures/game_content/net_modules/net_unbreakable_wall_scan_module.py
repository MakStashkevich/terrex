from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class NetUnbreakableWallScanModule(NetServerModule):
    def __init__(self, player_id: int, inside_unbreakable_walls: bool):
        self.player_id = player_id
        self.inside_unbreakable_walls = inside_unbreakable_walls

    @classmethod
    def read(cls, reader: Reader) -> 'NetUnbreakableWallScanModule':
        player_id = reader.read_byte()
        inside = reader.read_bool()
        return cls(player_id, inside)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_bool(self.inside_unbreakable_walls)
