"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.Slime

Slime-like blob shape: rounded top, tapered bottom.
"""

from .base import GenActionBulk, GenShape, GenAction, Point
import numpy as np
from math import sqrt

class Slime(GenShape):
    """Slime blob shape with scalable X/Y dimensions."""

    def __init__(self, radius: int, x_scale: float = 1.0, y_scale: float = 1.0, quit_on_fail: bool = False):
        super().__init__(quit_on_fail)
        self._radius = radius
        self._xScale = x_scale
        self._yScale = y_scale

    def perform(self, origin: Point, action: GenAction) -> bool:
        num = float(self._radius)
        num1 = (self._radius + 1) ** 2
        use_bulk = isinstance(action, GenActionBulk) and not self._quitOnFail

        xs_all = []
        ys_all = []

        # Upper part (full ellipse)
        for i in range(origin.Y - int(num * self._yScale), origin.Y + 1):
            y = (i - origin.Y) / self._yScale
            width = int(min(self._radius * self._xScale, self._xScale * sqrt(num1 - y * y)))
            if use_bulk:
                xs_all.append(np.arange(origin.X - width, origin.X + width + 1))
                ys_all.append(np.full(2 * width + 1, i))
            else:
                for j in range(origin.X - width, origin.X + width + 1):
                    if not self.unit_apply(action, origin, j, i) and self._quitOnFail:
                        return False

        # Lower part (tapered, half height)
        for k in range(origin.Y + 1, origin.Y + int(num * self._yScale * 0.5)):
            y1 = (k - origin.Y) * (2.0 / self._yScale)
            width = int(min(self._radius * self._xScale, self._xScale * sqrt(max(0, num1 - y1 * y1))))
            if use_bulk:
                xs_all.append(np.arange(origin.X - width, origin.X + width + 1))
                ys_all.append(np.full(2 * width + 1, k))
            else:
                for l in range(origin.X - width, origin.X + width + 1):
                    if not self.unit_apply(action, origin, l, k) and self._quitOnFail:
                        return False

        if use_bulk and xs_all:
            xs = np.concatenate(xs_all)
            ys = np.concatenate(ys_all)
            return action.apply_bulk(xs, ys)

        return True
