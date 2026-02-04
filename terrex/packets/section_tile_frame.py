from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class SectionTileFrame(Packet):
    id = PacketIds.SECTION_TILE_FRAME.value

    def __init__(self, start_x: int = 0, start_y: int = 0, end_x: int = 0, end_y: int = 0):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def read(self, reader: Reader):
        self.start_x = reader.read_short()
        self.start_y = reader.read_short()
        self.end_x = reader.read_short()
        self.end_y = reader.read_short()

    def write(self, writer: Writer):
        writer.write_short(self.start_x)
        writer.write_short(self.start_y)
        writer.write_short(self.end_x)
        writer.write_short(self.end_y)

SectionTileFrame.register()