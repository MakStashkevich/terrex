from dataclasses import dataclass

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


@dataclass
class HitSwitch:
    x: int
    y: int

    @classmethod
    def read(cls, reader: Reader) -> 'HitSwitch':
        return cls(
            reader.read_short(),
            reader.read_short(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_short(self.x)
        writer.write_short(self.y)


class PacketHitSwitch(SyncPacket):
    id = PacketIds.HIT_SWITCH

    def read(self, reader: Reader) -> None:
        self.data = HitSwitch.read(reader)

    def write(self, writer: Writer, data: HitSwitch) -> None:
        data.write(writer)


PacketHitSwitch.register()
