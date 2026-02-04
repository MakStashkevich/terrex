from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Writer

class RequestEssentialTiles(ClientPacket):
    id = PacketIds.REQUEST_ESSENTIAL_TILES.value

    def __init__(self, spawn_x: int = -1, spawn_y: int = -1):
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

    def write(self, writer: Writer):
        writer.write_short(self.spawn_x)
        writer.write_short(self.spawn_y)

RequestEssentialTiles.register()