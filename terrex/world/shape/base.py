"""
Ported from Terraria source: Terraria.WorldBuilding.GenShape and related base classes.

Original C# code adapted to Python with numpy optimizations for bulk operations.
"""

from dataclasses import dataclass
import numpy as np

@dataclass
class Point:
    """Equivalent to Microsoft.Xna.Framework.Point"""
    X: int
    Y: int

@dataclass
class RectangleArea:
    """Equivalent to Microsoft.Xna.Framework.Rectangle (using left/top instead of X/Y)"""
    left: int = 0
    top: int = 0
    width: int = 0
    height: int = 0

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height


class GenAction:
    """Base action applied to tile (x,y). Returns False on error."""
    def apply(self, x: int, y: int) -> bool:
        """
        Apply action to a single point.
        Returns False if operation failed.
        """
        raise NotImplementedError("Override apply()")


class GenShape:
    """Base shape. Perform generates points for action."""
    def __init__(self, quit_on_fail: bool = False):
        self._quitOnFail = quit_on_fail

    def unit_apply(self, action: GenAction, origin: Point, x: int, y: int) -> bool:
        """Internal UnitApply from C#."""
        return action.apply(x, y)

    def perform(self, origin: Point, action: GenAction) -> bool:
        """
        Execute shape: iterate over all points and apply action.
        Returns False if quit_on_fail and error.
        """
        raise NotImplementedError("Override Perform()")


class GenActionBulk(GenAction):
    """Base class for vectorized actions (numpy apply_bulk)."""
    def apply_bulk(self, xs: np.ndarray, ys: np.ndarray) -> bool:
        """
        Bulk application.
        Fallback: loop self.apply.
        """
        raise NotImplementedError("Override in subclass")


# Example usage:
# class BulkSetTile(GenActionBulk):
#     def __init__(self, world: np.ndarray, value):
#         self.world = world
#         self.value = value
#
#     def apply_bulk(self, xs, ys):
#         self.world[ys, xs] = self.value
#         return True
