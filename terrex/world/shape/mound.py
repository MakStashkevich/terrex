"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.Mound

Parabolic mound/hill shape.
"""

from .base import GenActionBulk, GenShape, GenAction, Point
import numpy as np

class Mound(GenShape):
    """Parabolic mound/hill shape with given half-width base and max height."""

    def __init__(self, half_width: int, height: int, quit_on_fail: bool = False):
        super().__init__(quit_on_fail)
        self._halfWidth = half_width
        self._height = height

    def Perform(self, origin: Point, action: GenAction) -> bool:
        half_w = float(self._halfWidth)
        xs_all = []
        ys_all = []

        # Fast bulk path
        use_bulk = isinstance(action, GenActionBulk) and not self._quitOnFail

        for i in range(-self._halfWidth, self._halfWidth + 1):
            # Parabolic height calculation (inverted parabola)
            num2 = int(
                -((self._height + 1) / (half_w * half_w)) * ((i + half_w) * (i - half_w))
            )
            num2 = max(0, min(self._height, num2))
            if use_bulk:
                xs = np.full(num2, origin.X + i)
                ys = np.arange(origin.Y - num2, origin.Y)
                xs_all.append(xs)
                ys_all.append(ys)
            else:
                for j in range(num2):
                    if not self.UnitApply(action, origin, origin.X + i, origin.Y - j) and self._quitOnFail:
                        return False

        if use_bulk and xs_all:
            xs = np.concatenate(xs_all)
            ys = np.concatenate(ys_all)
            return action.apply_bulk(xs, ys)

        return True
