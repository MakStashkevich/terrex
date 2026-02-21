from __future__ import annotations
from typing import Callable, Optional, TypeVar, Dict, Tuple

T = TypeVar("T")


class TileStack:
    def __init__(self) -> None:
        self._tiles: Dict[Tuple[int, int], T] = {}

    def get(self, x: int, y: int) -> Optional[T]:
        return self._tiles.get((x, y), None)

    def set(self, x: int, y: int, tile: T) -> None:
        self._tiles[(x, y)] = tile
