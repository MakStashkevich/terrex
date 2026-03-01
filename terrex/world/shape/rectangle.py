"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.Rectangle

Exact port with numpy meshgrid for bulk vectorized actions.
"""

import numpy as np

from .base import GenAction, GenActionBulk, GenShape, Point


class Rectangle(GenShape):
    """Rectangular area shape."""

    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def __init__(
        self, x: int = 0, y: int = 0, width: int = 0, height: int = 0, quit_on_fail: bool = False
    ):
        super().__init__(quit_on_fail)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def perform(self, origin: Point, action: GenAction) -> bool:
        # Numpy fast path for vectorized actions
        if isinstance(action, GenActionBulk):
            xs = np.arange(origin.x + self._area.left, origin.x + self._area.right)
            ys = np.arange(origin.y + self._area.top, origin.y + self._area.bottom)
            grid_x, grid_y = np.meshgrid(xs, ys)
            return action.apply_bulk(grid_x, grid_y)

        # Exact C# logic
        for i in range(origin.x + self._area.left, origin.x + self._area.right):
            for j in range(origin.y + self._area.top, origin.y + self._area.bottom):
                if not self.unit_apply(action, origin, i, j) and self._quitOnFail:
                    return False
        return True
