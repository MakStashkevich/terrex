from typing import Type, TypeVar, Generic, Awaitable

from terrex.event.context import EventContext
from ..types import BaseEvent


E = TypeVar("E", bound=BaseEvent)


class EventFilter(Generic[E]):
    _event_type: Type[E]

    async def matches(self, ctx: EventContext) -> E | None:
        raise NotImplementedError

    def __and__(self, other: "EventFilter[E]") -> "EventFilter[E]":
        from .combinators import AndFilter

        return AndFilter(self, other)

    def __or__(self, other: "EventFilter[E]") -> "EventFilter[E]":
        from .combinators import OrFilter

        return OrFilter(self, other)


class EventTypeFilter(EventFilter[E]):
    def __init__(self, event_type: Type[E]):
        self._event_type = event_type

    async def matches(self, ctx: EventContext) -> E | None:
        if isinstance(ctx.event, self._event_type):
            return ctx.event
        return None


class StopPropagation(Exception):
    pass
