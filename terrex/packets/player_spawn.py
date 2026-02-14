from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class PlayerSpawn(ClientPacket):
    id = MessageID.PlayerSpawn

    def __init__(self, player_id: int = 0, spawn_x: float = -1.0, spawn_y: float = -1.0, respawn_time_remaining: int = 0, player_spawn_context: int = 0):
        self.player_id = player_id
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.respawn_time_remaining = respawn_time_remaining
        self.player_spawn_context = player_spawn_context

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_float(self.spawn_x)
        writer.write_float(self.spawn_y)
        writer.write_int(self.respawn_time_remaining)
        writer.write_byte(self.player_spawn_context)

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.spawn_x = reader.read_float()
        self.spawn_y = reader.read_float()
        self.respawn_time_remaining = reader.read_int()
        self.player_spawn_context = reader.read_byte()
