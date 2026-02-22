import re
from typing import Type
from terrex.event.context import EventContext
from terrex.event.types import ChatEvent
from .base import EventFilter


class NewMessage(EventFilter[ChatEvent]):
    _event_type: Type[ChatEvent] = ChatEvent

    def __init__(self, pattern: str | None = None):
        self.pattern = re.compile(pattern) if pattern else None

    async def matches(self, ctx: EventContext) -> ChatEvent | None:
        event = ctx.event
        if not isinstance(event, ChatEvent):
            return None

        if self.pattern:
            match = self.pattern.search(event.text)
            if not match:
                return None
            event.pattern_match = match

        return event
