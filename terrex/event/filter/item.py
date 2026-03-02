from collections.abc import Callable
from typing import TypeVar

from terrex.event.context import EventFilterContext
from terrex.event.types import (
    BaseEvent,
    ItemDroppedEvent,
    ItemDropUpdateEvent,
    ItemOwnerChangedEvent,
)

from .base import EventFilter

T = TypeVar("T", bound=BaseEvent)


class ItemEventFilter(EventFilter[T]):
    event_type: type[T]

    def __init__(self, event_type: type[T], predicate: Callable[[T, EventFilterContext], bool]):
        self.event_type = event_type
        self.predicate = predicate

    def matches(self, ctx: EventFilterContext) -> T | None:
        event = ctx.event
        if not isinstance(event, self.event_type):
            return None
        if not self.predicate(event, ctx):
            return None
        return event


# Fabrics
def ItemDrop(item_id: int | None = None) -> ItemEventFilter[ItemDroppedEvent]:
    return ItemEventFilter(
        ItemDroppedEvent, lambda e, ctx: True if item_id is None else e.item.item_id == item_id
    )


def UpdateItemDrop(item_id: int | None = None) -> ItemEventFilter[ItemDropUpdateEvent]:
    return ItemEventFilter(
        ItemDropUpdateEvent, lambda e, ctx: True if item_id is None else e.item.item_id == item_id
    )


def UpdateItemOwner(item_id: int | None = None) -> ItemEventFilter[ItemOwnerChangedEvent]:
    return ItemEventFilter(
        ItemOwnerChangedEvent, lambda e, ctx: True if item_id is None else e.item_id == item_id
    )
