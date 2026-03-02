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
      
    @property
    def left(self) -> int:
        return self.x
    
    @property
    def right(self) -> int:
        return self.x + self.width
    
    @property
    def top(self) -> int:
        return self.y
    
    @property
    def bottom(self) -> int:
        return self.y + self.height

    def perform(self, origin: Point, action: GenAction) -> bool:
        # Numpy fast path for vectorized actions
        if isinstance(action, GenActionBulk):
            xs = np.arange(origin.x + self.x, origin.x + self.right)
            ys = np.arange(origin.y + self.top, origin.y + self.bottom)
            grid_x, grid_y = np.meshgrid(xs, ys)
            return action.apply_bulk(grid_x, grid_y)

        # Exact C# logic
        for i in range(origin.x + self.left, origin.x + self.right):
            for j in range(origin.y + self.top, origin.y + self.bottom):
                if not self.unit_apply(action, origin, i, j) and self._quitOnFail:
                    return False
        return True
