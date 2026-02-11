"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.Circle
"""

from math import sqrt
import numpy as np
from .base import GenActionBulk, GenShape, GenAction, Point

class Circle(GenShape):
    """Elliptical (oval) shape with independent horizontal and vertical radius."""

    def __init__(self, horizontal_radius: int, vertical_radius: int = None, quit_on_fail: bool = False):
        super().__init__(quit_on_fail)
        if vertical_radius is None:
            vertical_radius = horizontal_radius
        self._horizontalRadius = horizontal_radius
        self._verticalRadius = vertical_radius

    def SetRadius(self, radius: int):
        """Set both horizontal and vertical radius to the given value."""
        self._horizontalRadius = radius
        self._verticalRadius = radius

    def Perform(self, origin: Point, action: GenAction) -> bool:
        num = (self._horizontalRadius + 1) ** 2

        # Fast bulk path for GenActionBulk
        if isinstance(action, GenActionBulk):
            xs_all = []
            ys_all = []
            for i in range(origin.Y - self._verticalRadius, origin.Y + self._verticalRadius + 1):
                y = self._horizontalRadius / self._verticalRadius * (i - origin.Y)
                v = num - y * y
                if v < 0:
                    continue
                num1 = min(self._horizontalRadius, int(sqrt(v)))
                xs = np.arange(origin.X - num1, origin.X + num1 + 1)
                ys = np.full_like(xs, i)
                xs_all.append(xs)
                ys_all.append(ys)
            if not xs_all:
                return True
            return action.apply_bulk(np.concatenate(xs_all), np.concatenate(ys_all))

        # Exact C# path (pixel-perfect)
        for i in range(origin.Y - self._verticalRadius, origin.Y + self._verticalRadius + 1):
            y = self._horizontalRadius / self._verticalRadius * (i - origin.Y)
            v = num - y * y
            if v < 0:
                continue
            num1 = min(self._horizontalRadius, int(sqrt(v)))
            for j in range(origin.X - num1, origin.X + num1 + 1):
                if not self.UnitApply(action, origin, j, i) and self._quitOnFail:
                    return False
        return True
