from typing import Type, TypeVar, Generic, Awaitable

from terrex.event.context import EventContext
from .types import BaseEvent


class EventFilter:
    _event_type: BaseEvent

    async def matches(self, ctx: EventContext) -> BaseEvent | None:
        raise NotImplementedError

    def __and__(self, other: "EventFilter") -> "EventFilter":
        from .combinators import AndFilter

        return AndFilter(self, other)

    def __or__(self, other: "EventFilter") -> "EventFilter":
        from .combinators import OrFilter

        return OrFilter(self, other)


class StopPropagation(Exception):
    pass
