"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.Rectangle

Exact port with numpy meshgrid for bulk vectorized actions.
"""

import numpy as np

from .base import GenAction, GenActionBulk, GenShape, Point, RectangleArea


class Rectangle(GenShape):
    """Rectangular area shape."""

    def __init__(self, area: RectangleArea | None = None, quit_on_fail: bool = False):
        super().__init__(quit_on_fail)
        self._area = area or RectangleArea()

    @property
    def width(self) -> int:
        return self._area.width

    @width.setter
    def width(self, value: int) -> None:
        self._area.width = value

    @property
    def height(self) -> int:
        return self._area.height

    @height.setter
    def height(self, value: int) -> None:
        self._area.height = value

    @property
    def x(self) -> int:
        return self._area.left

    @property
    def y(self) -> int:
        return self._area.top

    @classmethod
    def from_size(cls, width: int, height: int, quit_on_fail: bool = False):
        """Constructor matching C#: Rectangle(int width, int height)"""
        return cls(RectangleArea(0, 0, width, height), quit_on_fail)

    def SetArea(self, area: RectangleArea):
        """SetArea as in C#"""
        self._area = area

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
