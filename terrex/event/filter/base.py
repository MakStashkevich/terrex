from typing import Generic, TypeVar

from terrex.event.context import EventFilterContext

from ..types import BaseEvent

E = TypeVar("E", bound=BaseEvent)


class EventFilter(Generic[E]):
    event_type: type[E]

    def matches(self, ctx: EventFilterContext) -> E | None:
        raise NotImplementedError

    def __and__(self, other: "EventFilter[E]") -> "EventFilter[E]":
        from .combinators import AndFilter

        return AndFilter(self, other)

    def __or__(self, other: "EventFilter[E]") -> "EventFilter[E]":
        from .combinators import OrFilter

        return OrFilter(self, other)


class EventTypeFilter(EventFilter[E]):
    def __init__(self, event_type: type[E]):
        self.event_type = event_type

    def matches(self, ctx: EventFilterContext) -> E | None:
        if isinstance(ctx.event, self.event_type):
            return ctx.event
        return None


class StopPropagation(Exception):
    pass
