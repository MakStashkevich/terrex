import re

from terrex.event.context import EventContext
from terrex.event.types import BaseEvent
from .base import EventFilter
from .types import ChatEvent

class NewMessage(EventFilter):
    _event_type = ChatEvent

    def __init__(self, pattern: str | None = None):
        self.pattern = re.compile(pattern) if pattern else None

    async def matches(self, ctx: EventContext) -> ChatEvent | None:
        if not isinstance(ctx.event, ChatEvent):
            return None
        if self.pattern:
            match = self.pattern.search(ctx.event.text)
            if not match:
                return None
            ctx.event.pattern_match = match
        return ctx.event