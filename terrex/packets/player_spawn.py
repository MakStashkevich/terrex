from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class PlayerSpawn(ClientPacket):
    id = MessageID.PlayerSpawn

    def __init__(
        self,
        player_id: int = 0,
        spawn_x: float = -1.0,
        spawn_y: float = -1.0,
        respawn_time_remaining: int = 0,
        number_of_deaths_pve: int = 0,
        number_of_deaths_pvp: int = 0,
        team_id: int = 0,
        player_spawn_context: int = 0,
    ):
        self.player_id = player_id
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.respawn_time_remaining = respawn_time_remaining
        self.number_of_deaths_pve = number_of_deaths_pve
        self.number_of_deaths_pvp = number_of_deaths_pvp
        self.team_id = team_id
        self.player_spawn_context = player_spawn_context

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.spawn_x)
        writer.write_short(self.spawn_y)
        writer.write_int(self.respawn_time_remaining)
        writer.write_short(self.number_of_deaths_pve)
        writer.write_short(self.number_of_deaths_pvp)
        writer.write_byte(self.team_id)
        writer.write_byte(self.player_spawn_context)

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.spawn_x = reader.read_short()
        self.spawn_y = reader.read_short()
        self.respawn_time_remaining = reader.read_int()
        self.number_of_deaths_pve = reader.read_short()
        self.number_of_deaths_pvp = reader.read_short()
        self.team_id = reader.read_byte()
        self.player_spawn_context = reader.read_byte()
