from collections.abc import Callable

from terrex.event.context import EventContext
from terrex.event.types import BlockedEvent, ChatEvent, ItemOwnerChangedEvent, LoginEvent

from .base import E, EventFilter, EventTypeFilter


class PlayerFilter(EventFilter[E]):
    _event_type: type[E]

    def __init__(self, event_type: type[E], predicate: Callable[[E, EventContext], bool]):
        self._event_type = event_type
        self.predicate = predicate

    def matches(self, ctx: EventContext) -> E | None:
        event = ctx.event
        if not isinstance(event, self._event_type):
            return None
        if not self.predicate(event, ctx):
            return None
        return event


# Player Fabrics
def OutgoingMessage() -> PlayerFilter[ChatEvent]:
    return PlayerFilter(ChatEvent, lambda e, ctx: e.player_id == ctx.player.id)


def IncomingMessage(player_id: int | None = None) -> PlayerFilter[ChatEvent]:
    return PlayerFilter(
        ChatEvent,
        lambda e, ctx: e.player_id != ctx.player.id
        and (True if player_id is None else e.player_id == player_id),
    )


def ItemOwnedByMe() -> PlayerFilter[ItemOwnerChangedEvent]:
    return PlayerFilter(ItemOwnerChangedEvent, lambda e, ctx: e.player_id == ctx.player.id)


def ItemOwnedByOther(player_id: int | None = None) -> PlayerFilter[ItemOwnerChangedEvent]:
    return PlayerFilter(
        ItemOwnerChangedEvent,
        lambda e, ctx: e.player_id != ctx.player.id
        and (True if player_id is None else e.player_id == player_id),
    )


# Other Player Filters
def LoginPlayer() -> EventTypeFilter[LoginEvent]:
    return EventTypeFilter(LoginEvent)


def BlockPlayer() -> EventTypeFilter[BlockedEvent]:
    return EventTypeFilter(BlockedEvent)
