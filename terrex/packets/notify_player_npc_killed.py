from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader

class NotifyPlayerNpcKilled(ServerPacket):
    id = PacketIds.NOTIFY_PLAYER_NPC_KILLED.value

    def __init__(self, npc_id: int = 0):
        self.npc_id = npc_id

    def read(self, reader: Reader) -> None:
        self.npc_id = reader.read_short()

    def handle(self, world, player, evman):
        pass

NotifyPlayerNpcKilled.register()