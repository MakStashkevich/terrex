from typing import Any

from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader
from terrex.structures.net_string import NetString


class Disconnect(ServerPacket):
    id = PacketIds.DISCONNECT.value

    def __init__(self, reason: NetString = NetString()):
        self.reason = reason

    def read(self, reader: Reader):
        self.reason = NetString.read(reader)

Disconnect.register()