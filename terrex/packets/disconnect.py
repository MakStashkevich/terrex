from typing import Any

from terrex.events.events import Event
from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader
from terrex.structures.net_string import NetworkText


class Disconnect(ServerPacket):
    id = PacketIds.DISCONNECT

    def __init__(self, reason: NetworkText = NetworkText()):
        self.reason = reason

    def read(self, reader: Reader):
        self.reason = NetworkText.read(reader)
        
    def handle(self, world, player, evman):
        evman.raise_event(Event.Blocked, self.reason)

Disconnect.register()