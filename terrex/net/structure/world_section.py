from dataclasses import dataclass, field
from typing import Any

from terrex.net.streamer import Reader
from terrex.net.tile_stack import TileStack
from terrex.world.world import World


@dataclass
class WorldSection:
    x_start: int = -1
    y_start: int = -1
    width: int = 200
    height: int = 150
    tiles: TileStack = field(default_factory=lambda: TileStack())
    chests: dict[int, Any] = field(default_factory=lambda: {})
    signs: dict[int, Any] = field(default_factory=lambda: {})
    tile_entities: list = field(default_factory=lambda: [])

    def read(self, reader: Reader, world: World) -> None:
        from terrex.net.structure.chest import Chest
        from terrex.net.structure.sign import Sign
        from terrex.net.structure.tile import Tile
        from terrex.entity.tile_entity import read_tile_entity

        tile: Tile | None = None
        rle: int = 0
        for y in range(self.y_start, self.y_start + self.height):
            for x in range(self.x_start, self.x_start + self.width):
                if rle == 0:
                    tile, rle = Tile.read(reader, world, x, y)
                    self.tiles.set(x, y, tile)
                else:
                    rle -= 1
                    copied_tile = world.tiles.get(x, y)
                    if copied_tile is None:
                        copied_tile = Tile()
                    copied_tile.copy_from(tile)
                    world.tiles.set(x, y, copied_tile)
                    self.tiles.set(x, y, copied_tile)

        if rle != 0:
            raise ValueError("WARNING: RLE not exhausted:", rle)

        n_chests = reader.read_short()
        for _ in range(n_chests):
            chest = Chest.read(reader)
            if 0 <= chest.index < 8000:
                world.chests[chest.index] = chest
                self.chests[chest.index] = chest

        n_signs = reader.read_short()
        for _ in range(n_signs):
            sign = Sign.read(reader)
            if 0 <= sign.index < 32000:
                world.signs[sign.index] = sign
                self.signs[sign.index] = sign

        n_entities = reader.read_short()
        for _ in range(n_entities):
            tile_entity = read_tile_entity(reader)
            world.tile_entities.append(tile_entity)
            self.tile_entities.append(tile_entity)

    def __repr__(self) -> str:
        return (
            f"WorldSection("
            + ", ".join(
                [
                    f"x_start={self.x_start}",
                    f"y_start={self.y_start}",
                    f"width={self.width}",
                    f"height={self.height}",
                    f"tiles_size={len(self.tiles)}",
                    f"chests_size={len(self.chests)}",
                    f"signs_size={len(self.signs)}",
                    f"tile_entities_size={len(self.tile_entities)})",
                ]
            )
            + ")"
        )
