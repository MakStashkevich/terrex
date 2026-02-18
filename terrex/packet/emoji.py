from terrex.packet.base import SyncPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class Emoji(SyncPacket):
    id = MessageID.Emoji

    def __init__(self, player_id: int = 0, emoticon: int = 0):
        self.player_id = player_id
        self.emoticon = emoticon

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.emoticon = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.emoticon)
