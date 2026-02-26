from dataclasses import dataclass

from terrex.net.structure.rgb import Rgb as Color
from terrex.world.world_gen import WorldGen


@dataclass
class MapTile:
    type: int
    color: int
    light: int

    def __str__(self):
        return f"MapTile(type={self.type}, color={self.color}, light={self.light})"


class MapHelper:
    # tile_colors: Dict[int, List[Color]] = {}
    # wall_colors: Dict[int, List[Color]] = {}
    color_lookup: list[Color] = []
    tile_option_counts: list[int] = []
    wall_option_counts: list[int] = []
    tile_lookup: list[int] = []
    wall_lookup: list[int] = []
    tile_position: int = 0
    wall_position: int = 0
    wall_range_start: int = 0
    wall_range_end: int = 0
    liquid_position: int = 0
    sky_position: int = 0
    dirt_position: int = 0
    rock_position: int = 0
    hell_position: int = 0
    snow_types: list[int] = []

    @classmethod
    def initialize(cls):
        from terrex.world.map_colors import add_colors

        add_colors()

    @classmethod
    def map_color(cls, tile_type: int, old_color: Color, color_type: int) -> Color:
        paint = WorldGen.paint_color(color_type)

        r = old_color.r / 255.0
        g = old_color.g / 255.0
        b = old_color.b / 255.0

        max_ch = r
        if g > max_ch:
            max_ch = g
        if b > max_ch:
            max_ch = b

        if color_type == 29:
            factor = b * 0.3
            new_color = Color(int(paint.r * factor), int(paint.g * factor), int(paint.b * factor))
        elif color_type == 30:
            # invert
            new_r = 255 - old_color.r
            new_g = 255 - old_color.g
            new_b = 255 - old_color.b
            if cls.wall_range_start <= tile_type <= cls.wall_range_end:
                new_r = int(new_r * 0.5)
                new_g = int(new_g * 0.5)
                new_b = int(new_b * 0.5)
            new_color = Color(new_r, new_g, new_b)
        else:
            new_color = Color(int(paint.r * max_ch), int(paint.g * max_ch), int(paint.b * max_ch))
        return new_color

    @classmethod
    def get_map_tile_xna_color(cls, tile: MapTile) -> Color:
        color = cls.color_lookup[tile.type]
        color_type = tile.color
        if color_type > 0:
            color = cls.map_color(tile.type, color, color_type)
        if tile.light == 255:
            return color
        light = tile.light / 255.0
        return Color(int(color.r * light), int(color.g * light), int(color.b * light))

    @classmethod
    def create_map_tile(
        cls, world, x: int, y: int, base_light: int, background_override: int = 0
    ) -> MapTile:
        from terrex.net.structure.tile import Tile
        from terrex.world.world import World

        if not isinstance(world, World):
            raise TypeError("world must be a World instance")

        tile = world.tiles.get(x, y)
        if not isinstance(tile, Tile):
            return MapTile(0, 0, 0)

        color = 0
        light = base_light
        base_type = 0
        base_option = 0
        color, light, base_type, base_option = cls.get_tile_type(
            world, x, y, tile, color, light, base_type, base_option
        )
        if base_type == 0:
            color, light, base_type, base_option = cls.get_wall_type(
                x, y, tile, color, light, base_type, base_option
            )
        if base_type == 0:
            color = 0
            light = base_light
            if background_override == 0:
                base_type, light = cls.get_background_type(world, x, y, light)
            else:
                base_type = background_override
        return MapTile(base_type + base_option, color, light)

    @classmethod
    def get_tile_type(
        cls,
        world,
        x: int,
        y: int,
        tile,
        new_color: int,
        new_light: int,
        base_type: int,
        base_option: int,
    ) -> tuple[int, int, int, int]:
        from terrex.net.structure.tile import Tile
        from terrex.world.world import World

        if not isinstance(world, World):
            raise TypeError("world must be a World instance")

        if not isinstance(tile, Tile):
            raise TypeError("tile must be a Tile instance")

        debug_show_unbreakable = getattr(cls, 'show_unbreakable_wall', False)
        if (not debug_show_unbreakable or tile.wall != 350) and tile.active:
            tile_type = tile.type
            base_type = cls.tile_lookup[tile_type]
            is_invisible_block = tile.invisible_block
            if tile.fullbright_block and not is_invisible_block:
                new_light = 255
            if is_invisible_block:
                base_type = 0
                return new_color, new_light, base_type, base_option
            if tile_type == 5:
                # stub WorldGen.IsThisAMushroomTree(x, y)
                # if False:
                #     base_option = 1
                new_color = tile.color
                return new_color, new_light, base_type, base_option
            special_parity = False
            if tile_type <= 51:
                if tile_type == 19:
                    if tile.frame_y == 864:
                        base_type = 0
                elif tile_type == 51:
                    special_parity = True
            elif tile_type == 184:
                if tile.frame_x // 22 == 10:
                    tile_type = 627
                    base_type = cls.tile_lookup[tile_type]
            elif tile_type == 697:
                special_parity = True
            if special_parity:
                if (x + y) % 2 == 0:
                    base_type = 0
            if base_type != 0:
                base_option = cls.get_tile_base_option(world, x, y, tile_type, tile, base_option)
                if tile_type == 160:
                    new_color = 0
                    return new_color, new_light, base_type, base_option
                new_color = tile.color
        return new_color, new_light, base_type, base_option

    @classmethod
    def get_wall_type(
        cls, x: int, y: int, tile, new_color: int, new_light: int, base_type: int, base_option: int
    ) -> tuple[int, int, int, int]:
        from terrex.id import WallID
        from terrex.net.structure.tile import Tile

        if not isinstance(tile, Tile):
            raise TypeError("tile must be a Tile instance")

        is_invisible_wall = tile.invisible_wall
        if tile.wall > 0 and tile.fullbright_wall and not is_invisible_wall:
            new_light = 255
        if tile.liquid > 32:
            num = tile.liquid_type
            base_type = cls.liquid_position + num
            return new_color, new_light, base_type, base_option
        if not tile.invisible_wall and tile.wall > 0 and tile.wall < WallID.Count:
            num1 = tile.wall
            base_type = cls.wall_lookup[num1]
            new_color = tile.wall_color
            if num1 <= 27:
                if num1 == 21:
                    new_color = 0
                    return new_color, new_light, base_type, base_option
                if num1 == 27:
                    base_option = x % 2
                    return new_color, new_light, base_type, base_option
                base_option = 0
                return new_color, new_light, base_type, base_option
            elif num1 - 88 > 5 and num1 != 168 and num1 != 241:
                base_option = 0
                return new_color, new_light, base_type, base_option
            new_color = 0
            return new_color, new_light, base_type, base_option
        return new_color, new_light, base_type, base_option

    @classmethod
    def get_background_type(cls, world, x: int, y: int, light: int) -> tuple[int, int]:
        from terrex.world.world import World

        if not isinstance(world, World):
            raise TypeError("world must be a World instance")

        if y < world.world_surface:
            if world.remix_world:
                light = 5
                return 100, light
            light = 255
            bg_type = cls.calc_sky_gradient(world, cls.sky_position, 256, y)
            return bg_type, light
        if y >= world.underworld_layer():
            return cls.hell_position, light
        num = 0

        if world.generating_world is False:
            # stub sceneArea.Contains(x, y)
            if False:
                scene_snowiness = getattr(cls, 'scene_snowiness', 0.0)
                num = int(max(0.0, min(scene_snowiness, 1.0)) * 255)
            else:
                found = False
                for x1 in range(x - 36, x + 31, 10):
                    if found:
                        break
                    for y1 in range(y - 36, y + 31, 10):
                        # type = Main.Map[x1, y1].Type  # minimap type, stub
                        map_tile = world.tiles.get(x1, y1)
                        map_type = map_tile.type if map_tile is not None else 0
                        for snow_type in cls.snow_types:
                            if snow_type == map_type:
                                num = 255
                                found = True
                                break
                        if found:
                            break

        if y < world.rock_layer:
            return cls.dirt_position + num, light
        return cls.rock_position + num, light

    @classmethod
    def get_tile_base_option(
        cls, world, x: int, y: int, tile_type: int, tile, base_option: int
    ) -> int:
        from terrex.net.structure.tile import Tile
        from terrex.world.world import World

        if not isinstance(world, World):
            raise TypeError("world must be a World instance")

        if not isinstance(tile, Tile):
            raise TypeError("tile must be a Tile instance")

        if tile_type == 89:
            frame_div = tile.frame_x // 54
            if frame_div in (0, 21, 23):
                base_option = 0
            elif frame_div == 43:
                base_option = 2
            else:
                base_option = 1
        elif tile_type in (160, 627, 628, 692):
            base_option = (x + y) % 9
        elif tile_type == 461:
            if world.players[world.my_player_id].zone.corrupt:
                base_option = 1
            elif world.players[world.my_player_id].zone.crimson:
                base_option = 2
            elif world.players[world.my_player_id].zone.hallow:
                base_option = 3
            # if Main.scene_metrics.zone_corrupt:
            #     base_option = 1
            # elif Main.scene_metrics.zone_crimson:
            #     base_option = 2
            # elif Main.scene_metrics.zone_hallow:
            #     base_option = 3
        elif tile_type == 80:
            evil, good, crimson = WorldGen.get_cactus_type(world, x, y, tile.frame_x, tile.frame_y)
            if evil:
                base_option = 1
            elif good:
                base_option = 2
            elif crimson:
                base_option = 3
            else:
                base_option = 0
        elif tile_type == 529:
            num9 = y + 1
            corrupt_count2, crimson_count2, hallowed_count2 = WorldGen.get_biome_influence(
                world, x, x, num9, num9
            )
            num10 = max(corrupt_count2, crimson_count2, hallowed_count2)
            if corrupt_count2 == 0 and crimson_count2 == 0 and hallowed_count2 == 0:
                base_option = (
                    1
                    if x < WorldGen.beach_distance
                    or x > world.max_tiles_x - WorldGen.beach_distance
                    else 0
                )
            elif hallowed_count2 == num10:
                base_option = 2
            elif crimson_count2 != num10:
                base_option = 4
            else:
                base_option = 3
        elif tile_type == 530:
            num2 = y - (tile.frame_y % 36) // 18 + 2
            num3 = x - (tile.frame_x % 54) // 18
            corrupt_count, crimson_count, hallowed_count = WorldGen.get_biome_influence(
                world, num3, num3 + 3, num2, num2
            )
            num4 = max(corrupt_count, crimson_count, hallowed_count)
            if corrupt_count != 0 or crimson_count != 0 or hallowed_count != 0:
                if hallowed_count == num4:
                    base_option = 1
                elif crimson_count != num4:
                    base_option = 3
                else:
                    base_option = 2
            else:
                base_option = 0
        elif tile_type == 19:
            num13 = tile.frame_y // 18
            base_option = 1 if num13 == 48 else 0
        elif tile_type == 15:
            num8 = tile.frame_y // 40
            base_option = 1 if num8 in (1, 20) else 0
        elif tile_type in (518, 519):
            base_option = tile.frame_y // 18
        elif tile_type == 4:
            base_option = 1 if tile.frame_x < 66 else 0
        elif tile_type == 572:
            base_option = tile.frame_y // 36
        elif tile_type in (21, 441):
            frame_div = tile.frame_x // 36
            if frame_div in (1, 2, 10, 13, 15):
                base_option = 1
            elif frame_div in (3, 4):
                base_option = 2
            elif frame_div == 6:
                base_option = 3
            elif frame_div in (11, 17):
                base_option = 4
            else:
                base_option = 0
        elif tile_type in (467, 468):
            num = tile.frame_x // 36
            if num in range(0, 12):
                base_option = num
            elif num in (12, 13, 15, 18):
                base_option = 10
            elif num in (14, 17):
                base_option = 7
            elif num == 16:
                base_option = 3
            else:
                base_option = 12
        elif tile_type == 560:
            num = tile.frame_x // 36
            base_option = num if 0 <= num <= 2 else 0
        elif tile_type in (28, 653):
            fy = tile.frame_y
            if fy < 144:
                base_option = 0
            elif fy < 252:
                base_option = 1
            elif fy < 360 or (900 <= fy < 1008):
                base_option = 2
            elif fy < 468:
                base_option = 3
            elif fy < 576:
                base_option = 4
            elif fy < 684:
                base_option = 5
            elif fy < 792:
                base_option = 6
            elif fy < 900:
                base_option = 8
            elif fy < 1008:
                base_option = 7
            elif fy < 1116:
                base_option = 0
            elif fy < 1224:
                base_option = 3
            else:
                base_option = 7
        elif tile_type == 27:
            base_option = 1 if tile.frame_y < 34 else 0
        elif tile_type in (31, 696):
            base_option = 1 if tile.frame_x >= 36 else 0
        elif tile_type in (26, 695):
            base_option = 1 if tile.frame_x >= 54 else 0
        elif tile_type == 137:
            fy_div = tile.frame_y // 18
            if fy_div in (1, 2, 3, 4):
                base_option = 1
            elif fy_div == 5:
                base_option = 2
            else:
                base_option = 0
        elif tile_type in (82, 83, 84):
            fx = tile.frame_x
            if fx < 18:
                base_option = 0
            elif fx < 36:
                base_option = 1
            elif fx < 54:
                base_option = 2
            elif fx < 72:
                base_option = 3
            elif fx < 90:
                base_option = 4
            elif fx < 108:
                base_option = 5
            else:
                base_option = 6
        elif tile_type == 591:
            base_option = tile.frame_x // 36
        elif tile_type == 105:
            fx = tile.frame_x
            if 1548 <= fx <= 1654:
                base_option = 1
            elif 1656 <= fx <= 1798:
                base_option = 2
            else:
                base_option = 0
        elif tile_type == 133:
            base_option = 0 if tile.frame_x < 52 else 1
        elif tile_type == 134:
            base_option = 0 if tile.frame_x < 28 else 1
        elif tile_type == 149:
            base_option = y % 3
        elif tile_type in (165, 693, 694):
            fx = tile.frame_x
            if fx < 54:
                base_option = 0
            elif fx < 106:
                base_option = 1
            elif fx >= 216:
                base_option = 1
            elif fx < 162:
                base_option = 2
            else:
                base_option = 3
        elif tile_type == 178:
            fx = tile.frame_x
            if fx < 18:
                base_option = 0
            elif fx < 36:
                base_option = 1
            elif fx < 54:
                base_option = 2
            elif fx < 72:
                base_option = 3
            elif fx < 90:
                base_option = 4
            elif fx < 108:
                base_option = 5
            else:
                base_option = 6
        elif tile_type == 184:
            fx = tile.frame_x
            if fx < 22:
                base_option = 0
            elif fx < 44:
                base_option = 1
            elif fx < 66:
                base_option = 2
            elif fx < 88:
                base_option = 3
            elif fx < 110:
                base_option = 4
            elif fx < 132:
                base_option = 5
            elif fx < 154:
                base_option = 6
            elif fx < 176:
                base_option = 7
            elif fx < 198:
                base_option = 8
            elif fx < 220:
                base_option = 9
            elif fx < 242:
                base_option = 10
        elif tile_type == 650:
            num = tile.frame_x // 18
            if num < 6 or num in (28, 29, 30, 31, 32):
                base_option = 0
            elif num < 12 or num in (33, 34, 35):
                base_option = 1
            elif num < 28:
                base_option = 2
            elif num < 48:
                base_option = 3
            elif num < 54:
                base_option = 4
            elif num < 72:
                base_option = 0
            elif num == 72:
                base_option = 1
            elif num < 78:
                base_option = 11
        elif tile_type == 649:
            num = tile.frame_x // 36
            num6 = tile.frame_y // 18 - 1
            num += num6 * 18
            if num < 6 or num in (19, 20, 21, 22, 23, 24, 33, 38, 39, 40):
                base_option = 0
            elif num < 16:
                base_option = 2
            elif num < 19 or num in (31, 32):
                base_option = 1
            elif num < 31:
                base_option = 3
            elif num < 38:
                base_option = 4
            elif num < 59:
                base_option = 0
            elif num < 62:
                base_option = 1
            elif num < 65:
                base_option = 11
        elif tile_type == 185:
            if tile.frame_y < 18:
                num = tile.frame_x // 18
                if num < 6 or num in (28, 29, 30, 31, 32):
                    base_option = 0
                elif num < 12 or num in (33, 34, 35):
                    base_option = 1
                elif num < 28:
                    base_option = 2
                elif num < 48:
                    base_option = 3
                elif num < 54:
                    base_option = 4
                elif num < 72:
                    base_option = 0
                elif num == 72:
                    base_option = 1
                elif num < 78:
                    base_option = 11
            else:
                num = tile.frame_x // 36
                num12 = tile.frame_y // 18 - 1
                num += num12 * 18
                if num < 6 or num in (19, 20, 21, 22, 23, 24, 33, 38, 39, 40):
                    base_option = 0
                elif num < 16:
                    base_option = 2
                elif num < 19 or num in (31, 32):
                    base_option = 1
                elif num < 31:
                    base_option = 3
                elif num < 38:
                    base_option = 4
                elif num < 59:
                    base_option = 0
                elif num < 62:
                    base_option = 1
                elif num < 65:
                    base_option = 11
        elif tile_type in (186, 647):
            num = tile.frame_x // 54
            if num < 7:
                base_option = 2
            elif num < 22 or num in (33, 34, 35):
                base_option = 0
            elif num < 25:
                base_option = 1
            elif num == 25:
                base_option = 5
            elif num < 32:
                base_option = 3
        elif tile_type in (187, 648):
            num = tile.frame_x // 54
            num7 = tile.frame_y // 36
            num += num7 * 36
            if num < 3 or num in (14, 15, 16):
                base_option = 0
            elif num < 6:
                base_option = 6
            elif num < 9:
                base_option = 7
            elif num < 14:
                base_option = 4
            elif num < 18:
                base_option = 4
            elif num < 23:
                base_option = 8
            elif num < 25:
                base_option = 0
            elif num < 29:
                base_option = 1
            elif num < 47:
                base_option = 0
            elif num < 50:
                base_option = 1
            elif num < 52:
                base_option = 10
            elif num < 55:
                base_option = 2
        elif tile_type == 227:
            base_option = tile.frame_x // 34
        elif tile_type == 129:
            base_option = 1 if tile.frame_x >= 324 else 0
        elif tile_type == 240:
            num = tile.frame_x // 54
            num14 = tile.frame_y // 54
            num += num14 * 36
            if (0 <= num <= 11) or (47 <= num <= 53) or num in (72, 73, 75):
                base_option = 0
            elif (num < 12 or num > 15) and (num < 18 or num > 35) and (num < 63 or num > 71):
                if num in (16, 17):
                    base_option = 2
                elif num in (41, 42, 43, 44, 45):
                    base_option = 3
                elif num == 46:
                    base_option = 4
                else:
                    base_option = 1
            else:
                base_option = 1
        elif tile_type == 242:
            num = tile.frame_y // 72
            base_option = 1 if tile.frame_x // 106 == 0 and 22 <= num <= 24 else 0
        elif tile_type == 440:
            num = tile.frame_x // 54
            base_option = min(num, 6)
        elif tile_type == 457:
            num = tile.frame_x // 36
            base_option = min(num, 4)
        elif tile_type == 453:
            num = tile.frame_x // 36
            base_option = min(num, 2)
        elif tile_type == 419:
            num = tile.frame_x // 18
            base_option = min(num, 2)
        elif tile_type == 428:
            num = tile.frame_y // 18
            base_option = min(num, 3)
        elif tile_type == 420:
            num = tile.frame_y // 18
            base_option = min(num, 5)
        elif tile_type == 423:
            num = tile.frame_y // 18
            base_option = min(num, 6)
        elif tile_type == 493:
            fx = tile.frame_x
            if fx < 18:
                base_option = 0
            elif fx < 36:
                base_option = 1
            elif fx < 54:
                base_option = 2
            elif fx < 72:
                base_option = 3
            elif fx < 90:
                base_option = 4
            else:
                base_option = 5
        elif tile_type == 548:
            base_option = 0 if tile.frame_x // 54 < 7 else 1
        elif tile_type == 597:
            num = tile.frame_x // 54
            base_option = num if num <= 10 else 0
        else:
            base_option = 0

        return base_option

    @classmethod
    def calc_sky_gradient(cls, world, sky_position: int, max_sky_gradients: int, y: int) -> int:
        from terrex.world.world import World

        if not isinstance(world, World):
            raise TypeError("world must be a World instance")

        world_surface = world.world_surface
        num = int((max_sky_gradients - 1) * (y / world_surface))
        num = min(255, num)  # byte
        return sky_position + num


MapHelper.initialize()
