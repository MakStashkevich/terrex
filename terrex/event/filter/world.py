from .base import EventTypeFilter
from terrex.event.types import TileSectionUpdateEvent


def UpdateTileSection() -> EventTypeFilter[TileSectionUpdateEvent]:
    return EventTypeFilter(TileSectionUpdateEvent)
