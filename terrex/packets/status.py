from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer
from terrex.structures.net_string import NetString


class Status(Packet):
    id = PacketIds.STATUS.value

    def __init__(self, status_id: int = 0, text: NetString = NetString(), flags: int = 0):
        self.status_id = status_id
        self.text = text
        self.flags = flags

    def read(self, reader: Reader):
        self.status_id = reader.read_int()
        self.text = NetString.read(reader)
        self.flags = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_int(self.status_id)
        self.text.write(writer)
        writer.write_byte(self.flags)

Status.register()