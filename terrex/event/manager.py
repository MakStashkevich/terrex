import asyncio
from collections.abc import Callable
from typing import Awaitable
from .filter.base import EventFilter
from .types import BaseEvent
from .dispatcher import Dispatcher


class EventManager:
    def __init__(self, dispatcher: Dispatcher):
        self._dispatcher = dispatcher

    def on_event(self, filter: EventFilter):
        def decorator(func: Callable[[BaseEvent], Awaitable[None]]) -> Callable[[BaseEvent], Awaitable[None]]:
            self._dispatcher.register(filter, func)
            return func

        return decorator

    def raise_event(self, event: BaseEvent):
        loop = asyncio.get_running_loop()
        loop.create_task(self._dispatcher.dispatch(event))

    def stop(self):
        self._dispatcher.shutdown()
