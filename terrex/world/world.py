from terrex.net.tile import Tile


class World:
    time: int = 0
    day_info: int = 0
    moon_phase: int = 0
    max_tiles_x: int = 0
    max_tiles_y: int = 0
    spawn_x: int = 0
    spawn_y: int = 0
    world_surface: int = 0
    rock_layer: int = 0
    world_id: int = 0
    world_name: str = ""
    game_mode: int = 0
    world_unique_id: list[int] = None
    world_generator_version: list[int] = None
    moon_type: int = 0
    tree_background: int = 0
    corruption_background: int = 0
    jungle_background: int = 0
    snow_background: int = 0
    hallow_background: int = 0
    crimson_background: int = 0
    desert_background: int = 0
    ocean_background: int = 0
    unknown_background: list[int] = None
    ice_back_style: int = 0
    jungle_back_style: int = 0
    hell_back_style: int = 0
    wind_speed_set: float = 0.0
    cloud_number: int = 0
    trees: list[int] = None
    tree_styles: list[int] = None
    cave_backs: list[int] = None
    cave_back_styles: list[int] = None
    forest_tree_top_styles: list[int] = None
    corruption_tree_top_style: int = 0
    jungle_tree_top_style: int = 0
    snow_tree_top_style: int = 0
    hallow_tree_top_style: int = 0
    crimson_tree_top_style: int = 0
    desert_tree_top_style: int = 0
    ocean_tree_top_style: int = 0
    glowing_mushroom_tree_top_style: int = 0
    underworld_tree_top_style: int = 0
    rain: float = 0.0
    event_info: int = 0
    ore_tiers_tiles: list[int] = None
    invasion_type: int = 0
    lobby_id: int = 0
    sandstorm_severity: float = 0.0

    # todo: move this
    items: object = {}
    item_owner_index: object = {}
    
    tiles = dict[int, dict[int, Tile]]

    def initialize_tiles(self, width, height):
        self.tiles = [[None for x in range(0, width)] for y in range(0, height)]
