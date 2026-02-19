from typing import Dict, List, Tuple, Optional
from PIL import Image
from dataclasses import dataclass
from terrex.net.rgb import Rgb as Color
from map_colors import add_colors
from terrex.world.world_gen import paint_color

@dataclass
class MapTile:
    type: int
    color: int
    light: int


class MapHelper:
    tile_colors: Dict[int, List[Color]] = {}
    wall_colors: Dict[int, List[Color]] = {}
    color_lookup: List[Color] = []
    tile_option_counts: Dict[int, Color] = {}
    wall_option_counts: Dict[int, Color] = {}
    tile_lookup: Dict[int, Color] = {}
    wall_lookup: Dict[int, Color] = {}
    tile_position: int = 0
    wall_position: int = 0
    wall_range_start: int = 0
    wall_range_end: int = 0
    liquid_position: int = 0
    sky_position: int = 0
    dirt_position: int = 0
    rock_position: int = 0
    hell_position: int = 0
    snow_types: List[Color] = []

    @classmethod
    def initialize(cls):
        add_colors(cls)

    @classmethod
    def draw_world_image(cls, tiles: List[List[int]], scale: int = 1) -> Image.Image:
        if not cls.color_lookup:
            cls.initialize()
        height = len(tiles)
        width = len(tiles[0]) if height > 0 else 0
        img = Image.new('RGB', (width * scale, height * scale))
        pixels = img.load()
        for y in range(height):
            for x in range(width):
                tile_id = tiles[y][x]
                color = cls.get_map_tile_xna_color(tile_id)
                rgb = (color.r, color.g, color.b)
                for sy in range(scale):
                    for sx in range(scale):
                        pixels[x * scale + sx, y * scale + sy] = rgb
        return img
        
    @classmethod
    def map_color(cls, tile_type: int, old_color: Color, color_type: int) -> Color:
        paint = paint_color(color_type)
        
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
            new_color = Color(
                float(paint.r * factor),
                float(paint.g * factor),
                float(paint.b * factor)
            )
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
            new_color = Color(
                int(paint.r * max_ch),
                int(paint.g * max_ch),
                int(paint.b * max_ch)
            )
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
        return Color(
            float(color.r * light),
            float(color.g * light),
            float(color.b * light)
        )
        
        
MapHelper.initialize()
