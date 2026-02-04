from enum import IntEnum
from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class DoorAction(IntEnum):
    OPEN_DOOR = 0
    CLOSE_DOOR = 1
    OPEN_TRAPDOOR = 2
    CLOSE_TRAPDOOR = 3
    OPEN_TALL_GATE = 4
    CLOSE_TALL_GATE = 5

    @classmethod
    def read(cls, reader: Reader) -> 'DoorAction':
        return cls(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.value)


class DoorToggle(SyncPacket):
    id = PacketIds.DOOR_TOGGLE.value

    def __init__(self, action: DoorAction = DoorAction.OPEN_DOOR, tile_x: int = 0, tile_y: int = 0, direction: int = 0):
        self.action = action
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.direction = direction

    def read(self, reader: Reader):
        self.action = DoorAction.read(reader)
        self.tile_x = reader.read_short()
        self.tile_y = reader.read_short()
        self.direction = reader.read_sbyte()

    def write(self, writer: Writer):
        self.action.write(writer)
        writer.write_short(self.tile_x)
        writer.write_short(self.tile_y)
        writer.write_sbyte(self.direction)

DoorToggle.register()