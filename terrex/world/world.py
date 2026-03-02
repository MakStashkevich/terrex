from terrex.item.item import Item


class World:
    def __init__(self):
        from terrex.entity.tile_entity.tile_entity import TileEntity
        from terrex.net.structure.chest import Chest
        from terrex.net.structure.sign import Sign
        from terrex.net.tile_stack import TileStack
        from terrex.player.player import Player

        self.time: int = 0
        self.day_info: int = 0
        self.moon_phase: int = 0
        self.max_tiles_x: int = 0
        self.max_tiles_y: int = 0
        self.spawn_x: int = 0
        self.spawn_y: int = 0
        self.world_surface: int = 0
        self.rock_layer: int = 0
        self.world_id: int = 0
        self.world_name: str = ""
        self.game_mode: int = 0
        self.world_unique_id: list[int] = []
        self.world_generator_version: list[int] = []
        self.moon_type: int = 0
        self.tree_background: int = 0
        self.corruption_background: int = 0
        self.jungle_background: int = 0
        self.snow_background: int = 0
        self.hallow_background: int = 0
        self.crimson_background: int = 0
        self.desert_background: int = 0
        self.ocean_background: int = 0
        self.unknown_background: list[int] = []
        self.ice_back_style: int = 0
        self.jungle_back_style: int = 0
        self.hell_back_style: int = 0
        self.wind_speed_set: float = 0.0
        self.cloud_number: int = 0
        self.trees: list[int] = []
        self.tree_styles: list[int] = []
        self.cave_backs: list[int] = []
        self.cave_back_styles: list[int] = []
        self.forest_tree_top_styles: list[int] = []
        self.corruption_tree_top_style: int = 0
        self.jungle_tree_top_style: int = 0
        self.snow_tree_top_style: int = 0
        self.hallow_tree_top_style: int = 0
        self.crimson_tree_top_style: int = 0
        self.desert_tree_top_style: int = 0
        self.ocean_tree_top_style: int = 0
        self.glowing_mushroom_tree_top_style: int = 0
        self.underworld_tree_top_style: int = 0
        self.rain: float = 0.0
        self.event_info: int = 0
        self.ore_tiers_tiles: list[int] = []
        self.invasion_type: int = 0
        self.lobby_id: int = 0
        self.sandstorm_severity: float = 0.0

        # todo: move this
        self.items: dict[int, Item] = {}
        self.item_owner_index: dict[int, int] = {}

        self.tiles: TileStack = TileStack()
        self.chests: dict[int, Chest] = {}
        self.signs: dict[int, Sign] = {}
        self.tile_entities: list[TileEntity] = []

        # always false because we connected to generated server world
        self.generating_world: bool = False

        # players info
        self.players: dict[int, Player] = {}
        self.my_player_id: int = -1

        # flags for special world seeds
        # https://terraria.wiki.gg/wiki/Special_world_seeds
        self.drunk_world: bool = False
        self.get_good_world: bool = False
        self.tenth_anniversary_world: bool = False
        self.dont_starve_world: bool = False
        self.not_the_bees_world: bool = False
        self.remix_world: bool = False
        self.no_traps_world: bool = False
        self.zenith_world: bool = False
        self.skyblock_world: bool = False
        self.vampire_seed: bool = False
        self.infected_seed: bool = False
        self.team_based_spawns_seed: bool = False
        self.dual_dungeons_seed: bool = False

    def underworld_layer(self) -> int:
        return self.max_tiles_y - 200
