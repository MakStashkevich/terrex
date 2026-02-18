from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader


class SyncRevengeMarker(ServerPacket):
    id = MessageID.SyncRevengeMarker

    def __init__(
        self,
        unique_id: int = 0,
        x: float = 0.0,
        y: float = 0.0,
        npc_id: int = 0,
        npc_hp_percent: float = 0.0,
        npc_type: int = 0,
        npc_ai: int = 0,
        coin_value: int = 0,
        base_value: float = 0.0,
        spawned_from_statue: bool = False,
    ):
        self.unique_id = unique_id
        self.x = x
        self.y = y
        self.npc_id = npc_id
        self.npc_hp_percent = npc_hp_percent
        self.npc_type = npc_type
        self.npc_ai = npc_ai
        self.coin_value = coin_value
        self.base_value = base_value
        self.spawned_from_statue = spawned_from_statue

    def read(self, reader: Reader) -> None:
        self.unique_id = reader.read_int()
        self.x = reader.read_float()
        self.y = reader.read_float()
        self.npc_id = reader.read_int()
        self.npc_hp_percent = reader.read_float()
        self.npc_type = reader.read_int()
        self.npc_ai = reader.read_int()
        self.coin_value = reader.read_int()
        self.base_value = reader.read_float()
        self.spawned_from_statue = reader.read_bool()

    def handle(self, world, player, evman):
        pass
