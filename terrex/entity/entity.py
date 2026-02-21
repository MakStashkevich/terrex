from abc import ABC

from terrex.net.structure.vec2 import Vec2


class Entity(ABC):
    id: int

    # todo: create position logic
    position: Vec2
    velocity: Vec2
    old_position: Vec2
    old_velocity: Vec2

    # direction
    direction: int = 1
    old_direction: int

    # size
    width: int
    height: int

    # wet
    wet: bool
    shimmer_wet: bool
    honey_wet: bool
    lava_wet: bool
    wet_count: int
