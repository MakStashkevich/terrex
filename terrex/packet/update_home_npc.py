from dataclasses import dataclass

from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


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


class UpdateHomeNPC(SyncPacket):
    id = MessageID.UpdateHomeNPC

    def read(self, reader: Reader) -> None:
        self.data = SetNpcHome.read(reader)

    def write(self, writer: Writer) -> None:
        self.data.write(writer)
