"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.Tail

Thick line (tail) using Bresenham algorithm with pixel/tile thickness.
Equivalent to Terraria's Utils.PlotTileTale.
"""

import math
from dataclasses import dataclass

import numpy as np

from .base import GenAction, GenActionBulk, GenShape, Point


@dataclass
class Vector2D:
    """Local port of ReLogic.Utilities.Vector2D"""

    X: float
    Y: float

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.X + other.X, self.Y + other.Y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.X * scalar, self.Y * scalar)

    __rmul__ = __mul__  # commutative multiplication


class Tail(GenShape):
    """Thick line from origin to end_offset with given width (in tiles)."""

    def __init__(self, width: float, end_offset: Vector2D, quit_on_fail: bool = False):
        """
        width: line thickness in tiles
        end_offset: end position offset from origin (in tiles)
        """
        super().__init__(quit_on_fail)
        self._width = width  # in tiles
        self._endOffset = end_offset

    def perform(self, origin: Point, action: GenAction) -> bool:
        # Compute tile coordinates (offsets are in world units? but scaled to tiles)
        start_tile = origin
        end_tile_x = int(origin.X + self._endOffset.X)
        end_tile_y = int(origin.Y + self._endOffset.Y)

        points = self._bresenham_thick(start_tile.X, start_tile.Y, end_tile_x, end_tile_y, self._width)

        # Fast-path for vectorized actions
        if isinstance(action, GenActionBulk) and not self._quitOnFail:
            xs = np.array([p[0] for p in points])
            ys = np.array([p[1] for p in points])
            return action.apply_bulk(xs, ys)

        # Standard loop
        for x, y in points:
            if not self.unit_apply(action, origin, x, y) and self._quitOnFail:
                return False
        return True

    def _bresenham_thick(self, x0: int, y0: int, x1: int, y1: int, width: float) -> list[tuple[int, int]]:
        """
        Bresenham line algorithm with thickness.
        width: thickness radius (full width ≈ 2*width + 1)
        Uses square approximation around each line point.
        """
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0

        half_w = int(math.floor(width / 2))

        while True:
            # Add thickness points (square around line point)
            for wx in range(-half_w, half_w + 1):
                for wy in range(-half_w, half_w + 1):
                    points.append((x + wx, y + wy))
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        return points
