from dataclasses import dataclass

from terrex.packet.base import SyncPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


@dataclass
class HitSwitchData:
    x: int
    y: int

    @classmethod
    def read(cls, reader: Reader) -> 'HitSwitchData':
        return cls(
            reader.read_short(),
            reader.read_short(),
        )

    def write(self, writer: Writer) -> None:
        writer.write_short(self.x)
        writer.write_short(self.y)


class HitSwitch(SyncPacket):
    id = MessageID.HitSwitch

    def read(self, reader: Reader) -> None:
        self.data = HitSwitchData.read(reader)

    def write(self, writer: Writer, data: HitSwitchData) -> None:
        data.write(writer)
