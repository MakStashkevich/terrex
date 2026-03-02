from collections.abc import Callable

from terrex.event.context import EventFilterContext
from terrex.event.types import (
    BlockedEvent,
    ChatEvent,
    ItemOwnerChangedEvent,
    LoginEvent,
    PlayerControlUpdateEvent,
)

from .base import E, EventFilter, EventTypeFilter


class PlayerFilter(EventFilter[E]):
    event_type: type[E]

    def __init__(self, event_type: type[E], predicate: Callable[[E, EventFilterContext], bool]):
        self.event_type = event_type
        self.predicate = predicate

    def matches(self, ctx: EventFilterContext) -> E | None:
        event = ctx.event
        if not isinstance(event, self.event_type):
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


def ControlBy(player_id: int | None = None) -> PlayerFilter[PlayerControlUpdateEvent]:
    return PlayerFilter(
        PlayerControlUpdateEvent,
        lambda e, ctx: e.player_id != ctx.player.id
        and (True if player_id is None else e.player_id == player_id),
    )


# Other Player Filters
def LoginPlayer() -> EventTypeFilter[LoginEvent]:
    return EventTypeFilter(LoginEvent)


def BlockPlayer() -> EventTypeFilter[BlockedEvent]:
    return EventTypeFilter(BlockedEvent)


def ControlPlayer() -> EventTypeFilter[PlayerControlUpdateEvent]:
    return EventTypeFilter(PlayerControlUpdateEvent)
