import asyncio
import concurrent.futures
import inspect
from collections.abc import Awaitable, Callable
from functools import partial
from typing import Any

from terrex.event.context import EventContext

from .filter.base import EventFilter, StopPropagation
from .types import BaseEvent


class Dispatcher:
    def __init__(self, terrex):
        from terrex.terrex import Terrex

        if not isinstance(terrex, Terrex):
            raise TypeError("terrex must be a Terrex instance")

        self._terrex = terrex
        self._handlers: dict[
            type[BaseEvent],
            list[
                tuple[
                    int, EventFilter[Any], Callable[[Any], Awaitable[None]] | Callable[[Any], None]
                ]
            ],
        ] = {}
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    def register(
        self,
        filter: EventFilter,
        callback: Callable[[Any], Awaitable[None]] | Callable[[Any], None],
        priority: int = 0,
    ) -> None:
        key = filter._event_type
        self._handlers.setdefault(key, []).append((priority, filter, callback))
        self._handlers[key].sort(key=lambda x: x[0], reverse=True)

    async def dispatch(self, event: BaseEvent) -> None:
        if not self._handlers:
            return

        loop = asyncio.get_running_loop()
        ctx = EventContext(self._terrex, event)

        for _, filter, callback in self._handlers.get(type(event), []):
            matched_event = filter.matches(ctx)
            if matched_event is None:
                continue

            try:
                sig = inspect.signature(callback)
                params = sig.parameters
                args = [matched_event] if len(params) == 1 else []

                if inspect.iscoroutinefunction(callback):
                    await callback(*args)
                else:
                    await loop.run_in_executor(self._executor, partial(callback, *args))
            except StopPropagation:
                break

    def shutdown(self):
        self._executor.shutdown(wait=True)
