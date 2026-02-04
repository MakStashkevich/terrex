from dataclasses import dataclass

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


@dataclass
class SetNpcHome:
    npc_id: int
    home_tile_x: int
    home_tile_y: int
    homeless: int

    @classmethod
    def read(cls, reader: Reader) -> 'SetNpcHome':
        return cls(
            reader.read_short(),
            reader.read_short(),
            reader.read_short(),
            reader.read_byte(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_short(self.npc_id)
        writer.write_short(self.home_tile_x)
        writer.write_short(self.home_tile_y)
        writer.write_byte(self.homeless)


class PacketSetNpcHome(SyncPacket):
    ID = PacketIds.NPC_HOME_UPDATE

    def read(self, reader: Reader) -> None:
        self.data = SetNpcHome.read(reader)

    def write(self, writer: Writer, data: SetNpcHome) -> None:
        data.write(writer)


PacketSetNpcHome.register()
