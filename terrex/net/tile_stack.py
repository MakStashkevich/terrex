from __future__ import annotations


class TileStack:
    def __init__(self) -> None:
        from terrex.net.structure.tile import Tile

        self._tiles: dict[tuple[int, int], Tile] = {}

    def get(self, x: int, y: int):
        return self._tiles.get((x, y), None)

    def set(self, x: int, y: int, tile) -> None:
        from terrex.net.structure.tile import Tile

        if not isinstance(tile, Tile):
            raise TypeError("tile must be a Tile instance")

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
