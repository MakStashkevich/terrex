from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer
from terrex.structures.net_string import NetString


class Disconnect(Packet):
    id = PacketIds.DISCONNECT.value

    def __init__(self, reason: NetString = NetString()):
        self.reason = reason

    def read(self, reader: Reader):
        self.reason = NetString.read(reader)

    def write(self, writer: Writer):
        self.reason.write(writer)

Disconnect.register()