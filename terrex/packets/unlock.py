from enum import IntEnum

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class UnlockType(IntEnum):
    CHEST = 1
    DOOR = 2


class Unlock(SyncPacket):
    id = PacketIds.UNLOCK

    def __init__(self, ty: UnlockType = UnlockType.CHEST, x: int = 0, y: int = 0):
        self.ty = ty
        self.x = x
        self.y = y

    def read(self, reader: Reader):
        self.ty = UnlockType(reader.read_byte())
        self.x = reader.read_short()
        self.y = reader.read_short()

    def write(self, writer: Writer):
        writer.write_byte(self.ty)
        writer.write_short(self.x)
        writer.write_short(self.y)


Unlock.register()
