from terrex.events.events import Event
from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.structures.localization.network_text import NetworkText
from terrex.util.streamer import Reader


class Kick(ServerPacket):
    id = MessageID.Kick

    def __init__(self, reason: NetworkText | None = None):
        self.reason = reason or NetworkText()

    def read(self, reader: Reader):
        self.reason = NetworkText.read(reader)

    def handle(self, world, player, evman):
        evman.raise_event(Event.Blocked, self.reason)
