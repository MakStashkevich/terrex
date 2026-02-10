from enum import IntEnum
from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class ChestAction(IntEnum):
    PLACE_CHEST = 0
    KILL_CHEST = 1
    PLACE_DRESSER = 2
    KILL_DRESSER = 3
    PLACE_CONTAINERS = 4
    KILL_CONTAINERS = 5

    @classmethod
    def read(cls, reader: Reader) -> 'ChestAction':
        return cls(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.value)


class PlaceChest(SyncPacket):
    id = PacketIds.PLACE_CHEST

    def __init__(self, action: ChestAction = ChestAction.PLACE_CHEST, tile_x: int = 0, tile_y: int = 0,
                 style: int = 0, chest_id_to_destroy: int = 0):
        self.action = action
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.style = style
        self.chest_id_to_destroy = chest_id_to_destroy

    def read(self, reader: Reader):
        self.action = ChestAction.read(reader)
        self.tile_x = reader.read_short()
        self.tile_y = reader.read_short()
        self.style = reader.read_short()
        self.chest_id_to_destroy = reader.read_short()

    def write(self, writer: Writer):
        self.action.write(writer)
        writer.write_short(self.tile_x)
        writer.write_short(self.tile_y)
        writer.write_short(self.style)
        writer.write_short(self.chest_id_to_destroy)

PlaceChest.register()