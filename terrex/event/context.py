from typing import TYPE_CHECKING

from terrex.event.types import BaseEvent

if TYPE_CHECKING:
    from terrex.terrex import Terrex


class EventContext:
    def __init__(self, terrex: "Terrex") -> None:
        self._terrex = terrex
        self.world = terrex.world
        self.player = terrex.player


class EventFilterContext(EventContext):
    def __init__(self, terrex: "Terrex", event: BaseEvent) -> None:
        super().__init__(terrex)
        self.event = event


class EventHandleContext(EventContext):
    def __init__(self, terrex: "Terrex") -> None:
        super().__init__(terrex)
        self.evman = terrex.evman


__all__ = ["EventFilterContext", "EventHandleContext"]
