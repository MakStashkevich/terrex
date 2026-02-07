from enum import IntFlag

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class SoundEffect(IntFlag):
    TREE_GROWTH = 0x01
    FAIRY = 0x02

    @classmethod
    def read(cls, reader: Reader) -> 'SoundEffect':
        return cls(reader.read_byte())

    def write(self, writer: Writer):
        writer.write_byte(self.value)


class GrowFx(SyncPacket):
    id = PacketIds.GROW_FX.value

    def __init__(self, effect: SoundEffect = SoundEffect.TREE_GROWTH, x: int = 0, y: int = 0, height: int = 0, tree_gore: int = 0):
        self.effect = effect
        self.x = x
        self.y = y
        self.height = height
        self.tree_gore = tree_gore

    def read(self, reader: Reader):
        self.effect = SoundEffect.read(reader)
        self.x = reader.read_int()
        self.y = reader.read_int()
        self.height = reader.read_byte()
        self.tree_gore = reader.read_short()

    def write(self, writer: Writer):
        self.effect.write(writer)
        writer.write_int(self.x)
        writer.write_int(self.y)
        writer.write_byte(self.height)
        writer.write_short(self.tree_gore)


GrowFx.register()
