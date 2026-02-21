from typing import Any


class Main:
    """
    Main Terrex class for save common info
    """

    # players info
    player: dict[int, Any] = {}
    my_player_id: int = -1

    # flags for special world seeds
    # https://terraria.wiki.gg/wiki/Special_world_seeds
    drunk_world: bool = False
    get_good_world: bool = False
    tenth_anniversary_world: bool = False
    dont_starve_world: bool = False
    not_the_bees_world: bool = False
    remix_world: bool = False
    no_traps_world: bool = False
    zenith_world: bool = False
    skyblock_world: bool = False
    vampire_seed: bool = False
    infected_seed: bool = False
    team_based_spawns_seed: bool = False
    dual_dungeons_seed: bool = False
