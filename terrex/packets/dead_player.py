from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader


class DeadPlayer(ServerPacket):
    id = PacketIds.DEAD_PLAYER.value

    def __init__(self, player_id: int = 0):
        self.player_id = player_id

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()


DeadPlayer.register()
