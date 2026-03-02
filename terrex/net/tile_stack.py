from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from terrex.net.structure.tile import Tile


class TileStack:
    def __init__(self) -> None:
        self._tiles: dict[tuple[int, int], "Tile"] = {}

    def get(self, x: int, y: int):
        return self._tiles.get((x, y), None)

    def set(self, x: int, y: int, tile: "Tile") -> None:
        self._tiles[(x, y)] = tile

    def values(self):
        return self._tiles.values()

    def items(self):
        return self._tiles.items()

    def keys(self):
        return self._tiles.keys()

    def __len__(self) -> int:
        return len(self._tiles)

    def __iter__(self):
        return iter(self._tiles.values())
