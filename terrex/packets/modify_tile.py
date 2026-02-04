from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class ModifyTile(Packet):
    id = PacketIds.MODIFY_TILE.value

    def __init__(
        self,
        action: int = 0,
        tile_x: int = 0,
        tile_y: int = 0,
        extra: int = 0,
        style: int = 0,
    ):
        self.action = action
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.extra = extra
        self.style = style

    def read(self, reader: Reader) -> None:
        self.action = reader.read_byte()
        self.tile_x = reader.read_short()
        self.tile_y = reader.read_short()
        self.extra = reader.read_short()
        self.style = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.action)
        writer.write_short(self.tile_x)
        writer.write_short(self.tile_y)
        writer.write_short(self.extra)
        writer.write_byte(self.style)

ModifyTile.register()