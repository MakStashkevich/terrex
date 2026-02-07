from enum import IntEnum
from typing import Optional

from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader


class SoundMode(IntEnum):
    STYLE = 1
    VOLUME_SCALE = 2
    PITCH_OFFSET = 3


class PlayLegacySound(ServerPacket):
    id = PacketIds.PLAY_LEGACY_SOUND.value

    def __init__(self, pos: Optional[Vec2] = None, sound_id: int = 0, mode: SoundMode = SoundMode.STYLE):
        self.pos = pos or Vec2(0.0, 0.0)
        self.sound_id = sound_id
        self.mode = mode

    def read(self, reader: Reader):
        self.pos = Vec2.read(reader)
        self.sound_id = reader.read_ushort()
        self.mode = SoundMode(reader.read_byte())


PlayLegacySound.register()
