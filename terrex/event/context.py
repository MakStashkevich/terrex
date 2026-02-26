from terrex.event.types import BaseEvent


class EventContext:
    def __init__(self, terrex, event: BaseEvent):
        from terrex.terrex import Terrex

        if not isinstance(terrex, Terrex):
            raise TypeError("terrex must be a Terrex instance")

        self.terrex = terrex
        self.world = terrex.world
        self.player = terrex.player

        self.event = event
