from dataclasses import dataclass

from terrex.net.enum.teleport_pylon_operation import TeleportPylonOperation
from terrex.net.enum.teleport_pylon_type import TeleportPylonType
from terrex.net.streamer import Reader, Writer

from .net_module import NetSyncModule


@dataclass()
class NetTeleportPylonModule(NetSyncModule):
    id: int = 7
    operation: TeleportPylonOperation = TeleportPylonOperation.HandleTeleportRequest
    x: int = -1
    y: int = -1
    pylon_type: TeleportPylonType = TeleportPylonType.SurfacePurity

    @classmethod
    def create(
        cls, operation: TeleportPylonOperation, x: int, y: int, pylon_type: TeleportPylonType
    ) -> "NetTeleportPylonModule":
        obj = cls()
        obj.operation = operation
        obj.x = x
        obj.y = y
        obj.pylon_type = pylon_type
        return obj

    def read(self, reader: Reader) -> None:
        self.operation = TeleportPylonOperation(reader.read_byte())
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.pylon_type = TeleportPylonType(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.operation.value)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_byte(self.pylon_type.value)
