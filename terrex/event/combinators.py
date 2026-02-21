from typing import List

from terrex.event.context import EventContext

from .base import EventFilter


class AndFilter(EventFilter):
    def __init__(self, *filters: EventFilter):
        if not filters:
            raise ValueError("AndFilter requires at least one filter")
        self.filters: List[EventFilter] = list(filters)

        # проверяем, что все фильтры имеют одинаковый event_type
        types = {getattr(f, "_event_type", None) for f in filters}
        if len(types) > 1:
            raise TypeError("All filters in AndFilter must have the same event type")
        self._event_type = types.pop()

    async def matches(self, ctx: EventContext):
        result = None
        for f in self.filters:
            result = await f.matches(ctx)
            if result is None:
                return None
        return result


class OrFilter(EventFilter):
    def __init__(self, *filters: EventFilter):
        if not filters:
            raise ValueError("OrFilter requires at least one filter")
        self.filters: List[EventFilter] = list(filters)

        types = {getattr(f, "_event_type", None) for f in filters}
        if len(types) > 1:
            raise TypeError("All filters in OrFilter must have the same event type")
        self._event_type = types.pop()

    async def matches(self, ctx: EventContext):
        for f in self.filters:
            result = await f.matches(ctx)
            if result is not None:
                return result
        return None
