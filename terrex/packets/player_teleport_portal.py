from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class PlayerTeleportPortal(SyncPacket):
    id = PacketIds.PLAYER_TELEPORT_PORTAL

    def __init__(self, player_id: int = 0, portal_color_index: int = 0, new_pos_x: float = 0.0, new_pos_y: float = 0.0, vel_x: float = 0.0, vel_y: float = 0.0):
        self.player_id = player_id
        self.portal_color_index = portal_color_index
        self.new_pos_x = new_pos_x
        self.new_pos_y = new_pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.portal_color_index = reader.read_short()
        self.new_pos_x = reader.read_float()
        self.new_pos_y = reader.read_float()
        self.vel_x = reader.read_float()
        self.vel_y = reader.read_float()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_short(self.portal_color_index)
        writer.write_float(self.new_pos_x)
        writer.write_float(self.new_pos_y)
        writer.write_float(self.vel_x)
        writer.write_float(self.vel_y)

    def handle(self, world, player, evman):
        pass

PlayerTeleportPortal.register()