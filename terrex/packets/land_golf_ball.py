from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class LandGolfBall(SyncPacket):
    id = PacketIds.LAND_GOLF_BALL_IN_CUP

    def __init__(self, player_id: int = 0, x: int = 0, y: int = 0, number_of_hits: int = 0, proj_id: int = 0):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.number_of_hits = number_of_hits
        self.proj_id = proj_id

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.number_of_hits = reader.read_ushort()
        self.proj_id = reader.read_ushort()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_ushort(self.number_of_hits)
        writer.write_ushort(self.proj_id)


LandGolfBall.register()
