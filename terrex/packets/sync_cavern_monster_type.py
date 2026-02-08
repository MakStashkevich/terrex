from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class SyncCavernMonsterType(SyncPacket):
    id = 136

    def __init__(self, types: list[int] = None):
        self.types = types or [0] * 6

    def read(self, reader: Reader) -> None:
        self.types = [reader.read_ushort() for _ in range(6)]

    def write(self, writer: Writer) -> None:
        for t in self.types:
            writer.write_ushort(t)

    def handle(self, world, player, evman):
        pass

SyncCavernMonsterType.register()