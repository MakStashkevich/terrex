from enum import IntEnum

from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class DodgeType(IntEnum):
    NINJA = 1
    SHADOW = 2


class PlayerDodge(SyncPacket):
    id = MessageID.PlayerDodge

    def __init__(self, player_id: int = 0, ty: DodgeType = DodgeType.NINJA):
        self.player_id = player_id
        self.ty = ty

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.ty = DodgeType(reader.read_byte())

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.ty)
