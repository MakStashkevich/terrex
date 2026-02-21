from terrex.event.context import EventContext

from .base import EventFilter
from .types import ChatEvent


class FromPlayer(EventFilter):
    _event_type = ChatEvent

    def __init__(self, player_id: int):
        self.player_id = player_id

    async def matches(self, ctx: EventContext) -> ChatEvent | None:
        if not isinstance(ctx.event, ChatEvent):
            return None
        if ctx.event.author_id != self.player_id:
            return None
        return ctx.event


class FromCurrentPlayer(EventFilter):
    _event_type = ChatEvent

    async def matches(self, ctx: EventContext) -> ChatEvent | None:
        if not isinstance(ctx.event, ChatEvent):
            return None
        if ctx.event.author_id != ctx.player.id:
            return None
        return ctx.event


class FromOtherPlayer(EventFilter):
    _event_type = ChatEvent

    async def matches(self, ctx: EventContext) -> ChatEvent | None:
        if not isinstance(ctx.event, ChatEvent):
            return None
        if ctx.event.author_id == ctx.player.id:
            return None
        return ctx.event
