from terrex.id.TileID import TileIDSets
from terrex.main import Main
from terrex.net.structure.rgb import Rgb as Color
from terrex.net.tile_npc_data import TileNPCData
from terrex.world.shape.base import Point
from terrex.world.shape.rectangle import Rectangle
from terrex.world.world import World


class WorldGen:
    ocean_distance: int = 250
    beach_distance: int = 380
    shimmer_safety_distance: int = 150

    @classmethod
    def paint_color(cls, color: int) -> Color:
        white = Color(255, 255, 255)
        num = color
        if num == 1 or num == 13:
            return Color(255, 0, 0)
        if num == 2 or num == 14:
            return Color(255, 127, 0)
        if num == 3 or num == 15:
            return Color(255, 255, 0)
        if num == 4 or num == 16:
            return Color(127, 255, 0)
        if num == 5 or num == 17:
            return Color(0, 255, 0)
        if num == 6 or num == 18:
            return Color(0, 255, 127)
        if num == 7 or num == 19:
            return Color(0, 255, 255)
        if num == 8 or num == 20:
            return Color(0, 127, 255)
        if num == 9 or num == 21:
            return Color(0, 0, 255)
        if num == 10 or num == 22:
            return Color(127, 0, 255)
        if num == 11 or num == 23:
            return Color(255, 0, 255)
        if num == 12 or num == 24:
            return Color(255, 0, 127)
        if num == 25:
            return Color(75, 75, 75)
        if num == 26:
            return Color(255, 255, 255)
        if num == 27:
            return Color(175, 175, 175)
        if num == 28:
            return Color(255, 178, 125)
        if num == 29:
            return Color(25, 25, 25)
        if num == 30:
            return Color(200, 200, 200, 150)
        return white

    @classmethod
    def get_biome_influence(cls, start_x: int, end_x: int, start_y: int, end_y: int) -> tuple[int, int, int]:
        corrupt_count = 0
        crimson_count = 0
        hallowed_count = 0

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                tile = World.tiles.get(x, y)
                if tile is not None:
                    if TileIDSets.Main.Corrupt[tile.type]:
                        corrupt_count += 1
                    if TileIDSets.Main.Crimson[tile.type]:
                        crimson_count += 1
                    if TileIDSets.Main.Hallow[tile.type]:
                        hallowed_count += 1

        return corrupt_count, crimson_count, hallowed_count

    @classmethod
    def get_cactus_type(cls, tile_x: int, tile_y: int, frame_x: int, frame_y: int) -> tuple[bool, bool, bool]:
        evil = False
        good = False
        crimson = False

        x = tile_x
        if frame_x == 36:
            x -= 1
        if frame_x == 54:
            x += 1
        if frame_x == 108:
            x = x + 1 if frame_y != 18 else x - 1

        y = tile_y
        flag = False

        if not cls.in_world(x, y, 2):
            return evil, good, crimson

        tile = World.tiles.get(x, y)
        if tile is None:
            return evil, good, crimson

        if tile.type == 80 and tile.active:
            flag = True

        while tile is not None and (not tile.active or not TileNPCData.tileSolid[tile.type] or not flag):
            if tile.type == 80 and tile.active:
                flag = True
            y += 1
            if y > tile_y + 20 or not cls.in_world(x, y, 2):
                break
            tile = World.tiles.get(x, y)

        if tile is not None and tile.active:
            if tile.type == 112:
                evil = True
            if tile.type == 116:
                good = True
            if tile.type == 234:
                crimson = True

        return evil, good, crimson

    @classmethod
    def in_world_point(cls, p: Point, fluff: int = 0) -> bool:
        return cls.in_world(p.x, p.y, fluff)

    @classmethod
    def in_world(cls, x: int, y: int, fluff: int = 0) -> bool:
        if x < fluff or x >= World.max_tiles_x - fluff or y < fluff or y >= World.max_tiles_y - fluff:
            return False
        return True

    @classmethod
    def in_world_rect(cls, rect: Rectangle, fluff: int = 0) -> bool:
        x = rect.x
        y = rect.y
        max_x = rect.x + rect.width
        max_y = rect.y + rect.height

        if x < fluff or max_x >= World.max_tiles_x - fluff or y < fluff or max_y >= World.max_tiles_y - fluff:
            return False
        return True
