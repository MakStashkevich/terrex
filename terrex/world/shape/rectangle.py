"""
Ported from Terraria source: Terraria.WorldBuilding.Shapes.Rectangle

Exact port with numpy meshgrid for bulk vectorized actions.
"""

from .base import GenActionBulk, GenShape, GenAction, Point, RectangleArea
import numpy as np

class Rectangle(GenShape):
    """Rectangular area shape."""

    def __init__(self, area: RectangleArea, quit_on_fail: bool = False):
        super().__init__(quit_on_fail)
        self._area = area

    @classmethod
    def from_size(cls, width: int, height: int, quit_on_fail: bool = False):
        """Constructor matching C#: Rectangle(int width, int height)"""
        return cls(RectangleArea(0, 0, width, height), quit_on_fail)

    def SetArea(self, area: RectangleArea):
        """SetArea as in C#"""
        self._area = area

    def Perform(self, origin: Point, action: GenAction) -> bool:
        # Numpy fast path for vectorized actions
        if isinstance(action, GenActionBulk):
            xs = np.arange(origin.X + self._area.left, origin.X + self._area.right)
            ys = np.arange(origin.Y + self._area.top, origin.Y + self._area.bottom)
            grid_x, grid_y = np.meshgrid(xs, ys)
            return action.apply_bulk(grid_x, grid_y)

        # Exact C# logic
        for i in range(origin.X + self._area.left, origin.X + self._area.right):
            for j in range(origin.Y + self._area.top, origin.Y + self._area.bottom):
                if not self.UnitApply(action, origin, i, j) and self._quitOnFail:
                    return False
        return True
