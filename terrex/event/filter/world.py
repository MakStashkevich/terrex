from terrex.event.types import WorldSectionUpdateEvent

from .base import EventTypeFilter


def UpdateTileSection() -> EventTypeFilter[WorldSectionUpdateEvent]:
    return EventTypeFilter(WorldSectionUpdateEvent)
