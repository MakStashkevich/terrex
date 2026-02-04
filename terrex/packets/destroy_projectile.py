from typing import Any

from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class DestroyProjectile(SyncPacket):
    id = PacketIds.DESTROY_PROJECTILE.value

    def __init__(self, projectile_id: int = 0, owner: int = 0):
        self.projectile_id = projectile_id
        self.owner = owner

    def read(self, reader: Reader):
        self.projectile_id = reader.read_short()
        self.owner = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.projectile_id)
        writer.write_byte(self.owner)

DestroyProjectile.register()