from typing import List, Any

from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader


class WorldData(ServerPacket):
    id = MessageID.WorldData

    def __init__(self, time: int = 0, day_info: int = 0, moon_phase: int = 0, max_tiles_x: int = 0, max_tiles_y: int = 0,
                 spawn_x: int = 0, spawn_y: int = 0, world_surface: int = 0, rock_layer: int = 0, world_id: int = 0,
                 world_name: str = "", game_mode: int = 0, world_unique_id: List[int] = None,
                 world_generator_version: List[int] = None, moon_type: int = 0, tree_background: int = 0,
                 corruption_background: int = 0, jungle_background: int = 0, snow_background: int = 0,
                 hallow_background: int = 0, crimson_background: int = 0, desert_background: int = 0,
                 ocean_background: int = 0, unknown_background: List[int] = None, ice_back_style: int = 0,
                 jungle_back_style: int = 0, hell_back_style: int = 0, wind_speed_set: float = 0.0,
                 cloud_number: int = 0, trees: List[int] = None, tree_styles: List[int] = None,
                 cave_backs: List[int] = None, cave_back_styles: List[int] = None,
                 forest_tree_top_styles: List[int] = None, corruption_tree_top_style: int = 0,
                 jungle_tree_top_style: int = 0, snow_tree_top_style: int = 0, hallow_tree_top_style: int = 0,
                 crimson_tree_top_style: int = 0, desert_tree_top_style: int = 0, ocean_tree_top_style: int = 0,
                 glowing_mushroom_tree_top_style: int = 0, underworld_tree_top_style: int = 0, rain: float = 0.0,
                 event_info: int = 0, ore_tiers_tiles: List[int] = None, invasion_type: int = 0, lobby_id: int = 0,
                 sandstorm_severity: float = 0.0):
        self.time = time
        self.day_info = day_info
        self.moon_phase = moon_phase
        self.max_tiles_x = max_tiles_x
        self.max_tiles_y = max_tiles_y
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.world_surface = world_surface
        self.rock_layer = rock_layer
        self.world_id = world_id
        self.world_name = world_name
        self.game_mode = game_mode
        self.world_unique_id = world_unique_id or [0] * 16
        self.world_generator_version = world_generator_version or [0, 0]
        self.moon_type = moon_type
        self.tree_background = tree_background
        self.corruption_background = corruption_background
        self.jungle_background = jungle_background
        self.snow_background = snow_background
        self.hallow_background = hallow_background
        self.crimson_background = crimson_background
        self.desert_background = desert_background
        self.ocean_background = ocean_background
        self.unknown_background = unknown_background or [0] * 5
        self.ice_back_style = ice_back_style
        self.jungle_back_style = jungle_back_style
        self.hell_back_style = hell_back_style
        self.wind_speed_set = wind_speed_set
        self.cloud_number = cloud_number
        self.trees = trees or [0, 0, 0]
        self.tree_styles = tree_styles or [0, 0, 0, 0]
        self.cave_backs = cave_backs or [0, 0, 0]
        self.cave_back_styles = cave_back_styles or [0, 0, 0, 0]
        self.forest_tree_top_styles = forest_tree_top_styles or [0, 0, 0, 0]
        self.corruption_tree_top_style = corruption_tree_top_style
        self.jungle_tree_top_style = jungle_tree_top_style
        self.snow_tree_top_style = snow_tree_top_style
        self.hallow_tree_top_style = hallow_tree_top_style
        self.crimson_tree_top_style = crimson_tree_top_style
        self.desert_tree_top_style = desert_tree_top_style
        self.ocean_tree_top_style = ocean_tree_top_style
        self.glowing_mushroom_tree_top_style = glowing_mushroom_tree_top_style
        self.underworld_tree_top_style = underworld_tree_top_style
        self.rain = rain
        self.event_info = event_info
        self.ore_tiers_tiles = ore_tiers_tiles or [0] * 7
        self.invasion_type = invasion_type
        self.lobby_id = lobby_id
        self.sandstorm_severity = sandstorm_severity

    def read(self, reader: Reader):
        self.time = reader.read_int()
        self.day_info = reader.read_byte()
        self.moon_phase = reader.read_byte()
        self.max_tiles_x = reader.read_short()
        self.max_tiles_y = reader.read_short()
        self.spawn_x = reader.read_short()
        self.spawn_y = reader.read_short()
        self.world_surface = reader.read_short()
        self.rock_layer = reader.read_short()
        self.world_id = reader.read_int()
        self.world_name = reader.read_dotnet_string()
        self.game_mode = reader.read_byte()
        self.world_unique_id = [reader.read_byte() for _ in range(16)]
        self.world_generator_version = [reader.read_int(), reader.read_int()]
        self.moon_type = reader.read_byte()
        self.tree_background = reader.read_byte()
        self.corruption_background = reader.read_byte()
        self.jungle_background = reader.read_byte()
        self.snow_background = reader.read_byte()
        self.hallow_background = reader.read_byte()
        self.crimson_background = reader.read_byte()
        self.desert_background = reader.read_byte()
        self.ocean_background = reader.read_byte()
        self.unknown_background = [reader.read_byte() for _ in range(5)]
        self.ice_back_style = reader.read_byte()
        self.jungle_back_style = reader.read_byte()
        self.hell_back_style = reader.read_byte()
        self.wind_speed_set = reader.read_float()
        self.cloud_number = reader.read_byte()
        self.trees = [reader.read_int() for _ in range(3)]
        self.tree_styles = [reader.read_byte() for _ in range(4)]
        self.cave_backs = [reader.read_int() for _ in range(3)]
        self.cave_back_styles = [reader.read_byte() for _ in range(4)]
        self.forest_tree_top_styles = [reader.read_byte() for _ in range(4)]
        self.corruption_tree_top_style = reader.read_byte()
        self.jungle_tree_top_style = reader.read_byte()
        self.snow_tree_top_style = reader.read_byte()
        self.hallow_tree_top_style = reader.read_byte()
        self.crimson_tree_top_style = reader.read_byte()
        self.desert_tree_top_style = reader.read_byte()
        self.ocean_tree_top_style = reader.read_byte()
        self.glowing_mushroom_tree_top_style = reader.read_byte()
        self.underworld_tree_top_style = reader.read_byte()
        self.rain = reader.read_float()
        self.event_info = reader.read_ulong()  # u64
        self.ore_tiers_tiles = [reader.read_short() for _ in range(7)]
        self.invasion_type = reader.read_sbyte()
        self.lobby_id = reader.read_ulong()
        self.sandstorm_severity = reader.read_float()

