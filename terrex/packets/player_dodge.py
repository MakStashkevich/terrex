from enum import IntEnum

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class DodgeType(IntEnum):
    NINJA = 1
    SHADOW = 2


class PlayerDodge(SyncPacket):
    id = PacketIds.PLAYER_DODGE

    def __init__(self, player_id: int = 0, ty: DodgeType = DodgeType.NINJA):
        self.player_id = player_id
        self.ty = ty

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.ty = DodgeType(reader.read_byte())

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.ty)


PlayerDodge.register()
