from __future__ import annotations
from typing import Optional, Dict, Tuple


class TileStack:
    def __init__(self) -> None:
        from terrex.net.structure.tile import Tile

        self._tiles: Dict[Tuple[int, int], Tile] = {}

    def get(self, x: int, y: int):
        return self._tiles.get((x, y), None)

    def set(self, x: int, y: int, tile) -> None:
        from terrex.net.structure.tile import Tile

        if not isinstance(tile, Tile):
            raise TypeError("tile must be a Tile instance")

        self._tiles[(x, y)] = tile

    def __len__(self) -> int:
        return len(self._tiles)
