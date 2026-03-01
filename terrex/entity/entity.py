import math
from abc import ABC

from terrex.net.structure.vec2 import Vec2
from terrex.world.shape.rectangle import Rectangle


class Entity(ABC):
    def __init__(self):
        self.id: int = 0  # whoAmI
        self.position: Vec2 = Vec2()
        self.velocity: Vec2 = Vec2()
        self.old_position: Vec2 = Vec2()
        self.old_velocity: Vec2 = Vec2()
        self.old_direction: int = 0
        self.direction: int = 1
        self.width: int = 0
        self.height: int = 0
        self.wet: bool = False
        self.shimmer_wet: bool = False
        self.honey_wet: bool = False
        self.lava_wet: bool = False
        self.wet_count: int = 0

    @property
    def any_wet(self) -> bool:
        if not self.wet and not self.lava_wet and not self.honey_wet:
            return self.shimmer_wet
        return True

    @property
    def visual_position(self) -> Vec2:
        return self.position

    @property
    def center(self) -> Vec2:
        return Vec2(self.position.x + self.width / 2.0, self.position.y + self.height / 2.0)

    @center.setter
    def center(self, value: Vec2) -> None:
        self.position = Vec2(value.x - self.width / 2.0, value.y - self.height / 2.0)

    @property
    def left(self) -> Vec2:
        return Vec2(self.position.x, self.position.y + self.height / 2.0)

    @left.setter
    def left(self, value: Vec2) -> None:
        self.position = Vec2(value.x, value.y - self.height / 2.0)

    @property
    def right(self) -> Vec2:
        return Vec2(self.position.x + self.width, self.position.y + self.height / 2.0)

    @right.setter
    def right(self, value: Vec2) -> None:
        self.position = Vec2(value.x - self.width, value.y - self.height / 2.0)

    @property
    def top(self) -> Vec2:
        return Vec2(self.position.x + self.width / 2.0, self.position.y)

    @top.setter
    def top(self, value: Vec2) -> None:
        self.position = Vec2(value.x - self.width / 2.0, value.y)

    @property
    def top_left(self) -> Vec2:
        return self.position

    @top_left.setter
    def top_left(self, value: Vec2) -> None:
        self.position = value

    @property
    def top_right(self) -> Vec2:
        return Vec2(self.position.x + self.width, self.position.y)

    @top_right.setter
    def top_right(self, value: Vec2) -> None:
        self.position = Vec2(value.x - self.width, value.y)

    @property
    def bottom(self) -> Vec2:
        return Vec2(self.position.x + self.width / 2.0, self.position.y + self.height)

    @bottom.setter
    def bottom(self, value: Vec2) -> None:
        self.position = Vec2(value.x - self.width / 2.0, value.y - self.height)

    @property
    def bottom_left(self) -> Vec2:
        return Vec2(self.position.x, self.position.y + self.height)

    @bottom_left.setter
    def bottom_left(self, value: Vec2) -> None:
        self.position = Vec2(value.x, value.y - self.height)

    @property
    def bottom_right(self) -> Vec2:
        return Vec2(self.position.x + self.width, self.position.y + self.height)

    @bottom_right.setter
    def bottom_right(self, value: Vec2) -> None:
        self.position = Vec2(value.x - self.width, value.y - self.height)

    @property
    def size(self) -> Vec2:
        return Vec2(float(self.width), float(self.height))

    @size.setter
    def size(self, value: Vec2) -> None:
        self.width = int(value.x)
        self.height = int(value.y)

    @property
    def hitbox(self) -> Rectangle:
        return Rectangle(int(self.position.x), int(self.position.y), self.width, self.height)

    @hitbox.setter
    def hitbox(self, value: Rectangle) -> None:
        self.position = Vec2(float(value.x), float(value.y))
        self.width = value.width
        self.height = value.height

    def angle_to(self, destination: Vec2) -> float:
        return math.atan2(destination.y - self.center.y, destination.x - self.center.x)

    def angle_from(self, source: Vec2) -> float:
        return math.atan2(self.center.y - source.y, self.center.x - source.x)

    def distance(self, other: Vec2) -> float:
        return self.center.distance_to(other)

    def distance_sq(self, other: Vec2) -> float:
        dx = self.center.x - other.x
        dy = self.center.y - other.y
        return dx * dx + dy * dy

    def direction_to(self, destination: Vec2) -> Vec2:
        diff_x = destination.x - self.center.x
        diff_y = destination.y - self.center.y
        length = math.sqrt(diff_x * diff_x + diff_y * diff_y)
        if length == 0:
            return Vec2()
        return Vec2(diff_x / length, diff_y / length)

    def direction_from(self, source: Vec2) -> Vec2:
        diff_x = self.center.x - source.x
        diff_y = self.center.y - source.y
        length = math.sqrt(diff_x * diff_x + diff_y * diff_y)
        if length == 0:
            return Vec2()
        return Vec2(diff_x / length, diff_y / length)

    def within_range(self, target: Vec2, max_range: float) -> bool:
        return self.distance_sq(target) <= max_range * max_range
