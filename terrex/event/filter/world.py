from .base import EventTypeFilter
from terrex.event.types import WorldSectionUpdateEvent


def UpdateTileSection() -> EventTypeFilter[WorldSectionUpdateEvent]:
    return EventTypeFilter(WorldSectionUpdateEvent)
