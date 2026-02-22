from typing import List, Generic
from terrex.event.context import EventContext
from .base import EventFilter, E


class AndFilter(EventFilter[E], Generic[E]):
    def __init__(self, *filters: EventFilter[E]):
        if not filters:
            raise ValueError("AndFilter requires at least one filter")

        self.filters: List[EventFilter[E]] = []

        # flatten nested AndFilter
        for f in filters:
            if isinstance(f, AndFilter):
                self.filters.extend(f.filters)
            else:
                self.filters.append(f)

        event_type = self.filters[0]._event_type
        for f in self.filters:
            if f._event_type is not event_type:
                raise TypeError("All filters in AndFilter must have the same event type")

        self._event_type = event_type

    async def matches(self, ctx: EventContext) -> E | None:
        result: E | None = None
        for f in self.filters:
            result = await f.matches(ctx)
            if result is None:
                return None
        return result

    def __repr__(self):
        return f"And({', '.join(repr(f) for f in self.filters)})"


class OrFilter(EventFilter[E], Generic[E]):
    def __init__(self, *filters: EventFilter[E]):
        if not filters:
            raise ValueError("OrFilter requires at least one filter")

        self.filters: List[EventFilter[E]] = []

        # flatten nested OrFilter
        for f in filters:
            if isinstance(f, OrFilter):
                self.filters.extend(f.filters)
            else:
                self.filters.append(f)

        event_type = self.filters[0]._event_type
        for f in self.filters:
            if f._event_type is not event_type:
                raise TypeError("All filters in OrFilter must have the same event type")

        self._event_type = event_type

    async def matches(self, ctx: EventContext) -> E | None:
        for f in self.filters:
            result = await f.matches(ctx)
            if result is not None:
                return result
        return None

    def __repr__(self):
        return f"Or({', '.join(repr(f) for f in self.filters)})"
