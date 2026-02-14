from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader

class TamperWithNPC(ServerPacket):
    id = MessageID.TamperWithNPC

    def __init__(self, npc_id: int = 0, set_npc_immunity: bool = False, immunity_time: int = 0, immunity_player_id: int = 0):
        self.npc_id = npc_id
        self.set_npc_immunity = set_npc_immunity
        self.immunity_time = immunity_time
        self.immunity_player_id = immunity_player_id

    def read(self, reader: Reader) -> None:
        self.npc_id = reader.read_ushort()
        self.set_npc_immunity = bool(reader.read_byte())
        if self.set_npc_immunity:
            self.immunity_time = reader.read_int()
            self.immunity_player_id = reader.read_short()

    def handle(self, world, player, evman):
        pass

