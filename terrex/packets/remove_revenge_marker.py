from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader

class RemoveRevengeMarker(ServerPacket):
    id = 127

    def __init__(self, unique_id: int = 0):
        self.unique_id = unique_id

    def read(self, reader: Reader) -> None:
        self.unique_id = reader.read_int()

    def handle(self, world, player, evman):
        pass

RemoveRevengeMarker.register()