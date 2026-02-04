from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class RequestSign(Packet):
    id = PacketIds.REQUEST_SIGN.value

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def read(self, reader: Reader):
        self.x = reader.read_short()
        self.y = reader.read_short()

    def write(self, writer: Writer):
        writer.write_short(self.x)
        writer.write_short(self.y)

RequestSign.register()