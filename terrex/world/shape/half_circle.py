"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.HalfCircle
"""

from math import sqrt

import numpy as np

from .base import GenAction, GenActionBulk, GenShape, Point


class HalfCircle(GenShape):
    """Half circle shape: upper half (default) or bottom half."""

    def __init__(self, radius: int, bottom_half: bool = False, quit_on_fail: bool = False):
        super().__init__(quit_on_fail)
        self._radius = radius
        self._bottomHalf = bottom_half

    def perform(self, origin: Point, action: GenAction) -> bool:
        num = (self._radius + 1) ** 2

        # Fast bulk path
        if isinstance(action, GenActionBulk):
            xs_all = []
            ys_all = []

            if self._bottomHalf:
                y_start, y_end = origin.y, origin.y + self._radius
            else:
                y_start, y_end = origin.y - self._radius, origin.y

            for i in range(y_start, y_end + 1):
                v = num - (i - origin.y) ** 2
                if v < 0:
                    continue
                num2 = min(self._radius, int(sqrt(v)))
                xs = np.arange(origin.x - num2, origin.x + num2 + 1)
                ys = np.full_like(xs, i)
                xs_all.append(xs)
                ys_all.append(ys)

            if not xs_all:
                return True

            return action.apply_bulk(np.concatenate(xs_all), np.concatenate(ys_all))

        # Standard path
        if self._bottomHalf:
            y_start, y_end = origin.y, origin.y + self._radius
        else:
            y_start, y_end = origin.y - self._radius, origin.y

        for i in range(y_start, y_end + 1):
            v = num - (i - origin.y) ** 2
            if v < 0:
                continue
            num2 = min(self._radius, int(sqrt(v)))
            for j in range(origin.x - num2, origin.x + num2 + 1):
                if not self.unit_apply(action, origin, j, i) and self._quitOnFail:
                    return False

        return True
