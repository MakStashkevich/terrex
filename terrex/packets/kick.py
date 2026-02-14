from typing import Any

from terrex.events.events import Event
from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader
from terrex.structures.localization.network_text import NetworkText


class Kick(ServerPacket):
    id = MessageID.Kick

    def __init__(self, reason: NetworkText = NetworkText()):
        self.reason = reason

    def read(self, reader: Reader):
        self.reason = NetworkText.read(reader)
        
    def handle(self, world, player, evman):
        evman.raise_event(Event.Blocked, self.reason)

