from terrex.net.bits_byte import BitsByte
from terrex.net.enum.teleport_pylon_type import TeleportPylonType
from terrex.net.enum.teleport_type import TeleportType
from terrex.packet.base import SyncPacket
from terrex.id import MessageID
from terrex.net.structure.vec2 import Vec2
from terrex.net.streamer import Reader, Writer


class TeleportEntityFlags:
    def __init__(
        self,
        server_synced: bool = False,
        player_teleport: bool = False,
        spawn_failed: bool = False,
        has_type_of_pylon: bool = False,
    ):
        self.flags: BitsByte = BitsByte()
        self.server_synced = server_synced
        self.player_teleport = player_teleport
        self.spawn_failed = spawn_failed
        self.has_type_of_pylon = has_type_of_pylon

    @classmethod
    def create(cls, flags: int = 0) -> None:
        tp_entity = cls()
        tp_entity.flags = flags
        return cls()

    @property
    def need_sync(self) -> bool:
        return not (self.server_synced or self.player_teleport)

    @property
    def server_synced(self) -> bool:
        return self.flags[0]

    @server_synced.setter
    def server_synced(self, val: bool):
        self.flags[0] = val

    @property
    def player_teleport(self) -> bool:
        return self.flags[1]

    @player_teleport.setter
    def player_teleport(self, val: bool):
        self.flags[1] = val

    @property
    def spawn_failed(self) -> bool:
        return self.flags[2]

    @spawn_failed.setter
    def spawn_failed(self, val: bool):
        self.flags[2] = val

    @property
    def has_type_of_pylon(self) -> bool:
        return self.flags[3]

    @has_type_of_pylon.setter
    def has_type_of_pylon(self, val: bool):
        self.flags[3] = val

    def __int__(self) -> int:
        return int(self.flags)

    def __repr__(self):
        return (
            f"TeleportFlags(server_synced={self.server_synced}, "
            f"player_teleport={self.player_teleport}, "
            f"spawn_failed={self.spawn_failed}, "
            f"has_type_of_pylon={self.has_type_of_pylon}, "
            f"need_sync={self.need_sync}, "
            f"value={int(self.flags):08b})"
        )


class TeleportEntity(SyncPacket):
    id = MessageID.TeleportEntity

    def __init__(
        self,
        server_synced: bool = False,
        player_teleport: bool = False,
        player_id: int = 0,
        position: Vec2 | None = None,
        type: TeleportType = TeleportType.TeleporterTile,
        pylon_type: TeleportPylonType = TeleportPylonType.SurfacePurity,
    ) -> None:
        self.flags: TeleportEntityFlags = TeleportEntityFlags(server_synced, player_teleport, has_type_of_pylon=pylon_type != TeleportPylonType.SurfacePurity)
        self.player_id: int = player_id
        self.position: Vec2 = position or Vec2(0, 0)
        self.teleport_type: int = type
        self.pylon_type: int = pylon_type

    def read(self, reader: Reader) -> None:
        self.flags = TeleportEntityFlags.create(reader.read_byte())
        self.player_id = reader.read_short()
        self.position.x = reader.read_float()
        self.position.y = reader.read_float()
        self.teleport_type = TeleportType(reader.read_byte())
        if self.flags.has_type_of_pylon:
            self.pylon_type = TeleportPylonType(reader.read_int())

    def write(self, writer: Writer) -> None:
        writer.write_byte(int(self.flags))
        writer.write_short(self.player_id)
        writer.write_float(self.position.x)
        writer.write_float(self.position.y)
        writer.write_byte(self.teleport_type)
        if self.flags.has_type_of_pylon:
            writer.write_int(self.pylon_type)
