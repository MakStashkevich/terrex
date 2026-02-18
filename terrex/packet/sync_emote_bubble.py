from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader


class SyncEmoteBubble(ServerPacket):
    id = MessageID.SyncEmoteBubble

    def __init__(self, emote_id: int = 0, anchor_type: int = 255, player_id: int = 0, emote_lifetime: int = 0, emote: int = 0, emote_metadata: int = 0):
        self.emote_id = emote_id
        self.anchor_type = anchor_type
        self.player_id = player_id
        self.emote_lifetime = emote_lifetime
        self.emote = emote
        self.emote_metadata = emote_metadata

    def read(self, reader: Reader) -> None:
        self.emote_id = reader.read_int()
        self.anchor_type = reader.read_byte()
        if self.anchor_type != 255:
            self.player_id = reader.read_ushort()
            self.emote_lifetime = reader.read_ushort()
            self.emote = reader.read_byte()
            if self.emote < 0:
                self.emote_metadata = reader.read_short()

    def handle(self, world, player, evman):
        pass
