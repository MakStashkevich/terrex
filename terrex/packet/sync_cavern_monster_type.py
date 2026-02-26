from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class SyncCavernMonsterType(SyncPacket):
    id = MessageID.SyncCavernMonsterType

    def __init__(self, types: list[int] | None = None):
        self.types = types or [0] * 6

    def read(self, reader: Reader) -> None:
        self.types = [reader.read_ushort() for _ in range(6)]

    def write(self, writer: Writer) -> None:
        for t in self.types:
            writer.write_ushort(t)
