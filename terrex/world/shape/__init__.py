"""
Shape module for world generation in Terrex.
"""

from .base import GenAction, GenShape, Point
from .circle import Circle
from .half_circle import HalfCircle
from .mound import Mound
from .rectangle import Rectangle
from .slime import Slime
from .tail import Tail

__all__ = [
    'Point',
    'GenAction',
    'GenShape',
    'Rectangle',
    'Circle',
    'HalfCircle',
    'Mound',
    'Slime',
    'Tail',
]
