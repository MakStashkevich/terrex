import zlib

from terrex.event.types import WorldSectionUpdateEvent
from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader


class TileSection(ServerPacket):
    id = MessageID.TileSection

    def read(self, reader: Reader) -> None:
        compressed_data = reader.remaining()
        decompressed = zlib.decompress(compressed_data, -zlib.MAX_WBITS)
        section_reader = Reader(decompressed)

        self.x_start = section_reader.read_int()
        self.y_start = section_reader.read_int()
        self.width = section_reader.read_short()
        self.height = section_reader.read_short()

        self.section_reader = section_reader

    async def handle(self, world, player, evman):
        if self.width < 0 or self.width > 200 or self.height < 0 or self.height > 150:
            return

        if not self.section_reader:
            return

        from terrex.net.structure.world_section import WorldSection

        section = WorldSection(self.x_start, self.y_start, self.width, self.height)
        section.read(self.section_reader, world)

        print(f"Loaded {section}")

        evman.raise_event(WorldSectionUpdateEvent(self, section))
