from terrex.event.event import Event
from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.localization.network_text import NetworkText
from terrex.net.streamer import Reader


class Kick(ServerPacket):
    id = MessageID.Kick

    def __init__(self, reason: NetworkText | None = None):
        self.reason = reason or NetworkText()

    def read(self, reader: Reader):
        self.reason = NetworkText.read(reader)

    def handle(self, world, player, evman):
        evman.raise_event(Event.Blocked, self.reason)
