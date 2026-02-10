from enum import IntEnum
from terrex.structures.game_content.teleport_pylon_type import TeleportPylonType
from terrex.util.streamer import Reader, Writer
from .base import NetSyncModule


class TeleportPylonOperation(IntEnum):
    AddForClient = 0
    RemoveForClient = 1
    HandleTeleportRequest = 2


class NetTeleportPylonModule(NetSyncModule):
    def __init__(self, operation: TeleportPylonOperation, x: int, y: int, pylon_type: TeleportPylonType):
        self.operation = operation
        self.x = x
        self.y = y
        self.pylon_type = pylon_type

    @classmethod
    def read(cls, reader: Reader) -> 'NetTeleportPylonModule':
        operation = TeleportPylonOperation(reader.read_byte())
        x = reader.read_short()
        y = reader.read_short()
        pylon_type = TeleportPylonType(reader.read_byte())
        return cls(operation, x, y, pylon_type)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.operation.value)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_byte(self.pylon_type.value)
