from dataclasses import dataclass, field

from terrex.net.vec2 import Vec2


@dataclass
class Item:
    item_id: int = -1
    net_id: int = -1
    position: Vec2 = field(default_factory=lambda: Vec2())
    velocity: Vec2 = field(default_factory=lambda: Vec2())
    prefix: int = 0
    stacks: int = 1
