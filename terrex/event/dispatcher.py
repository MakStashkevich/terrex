from collections.abc import Callable
from typing import Any, Awaitable, Dict, List, Tuple

from terrex.event.context import EventContext
from .types import BaseEvent
import asyncio
import inspect
import concurrent.futures

from .filter.base import EventFilter, StopPropagation


class Dispatcher:
    def __init__(self, terrex):
        from terrex.terrex import Terrex

        if not isinstance(terrex, Terrex):
            raise TypeError("terrex must be a Terrex instance")

        self._terrex = terrex
        self._handlers: Dict[type[BaseEvent], List[Tuple[int, EventFilter[Any], Callable[[Any], Awaitable[None]]]]] = {}
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    def register(
        self,
        filter: EventFilter,
        callback: Callable[[BaseEvent], Awaitable[None]] | Callable[[BaseEvent], None],
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
                    await loop.run_in_executor(self._executor, lambda: callback(*args))
            except StopPropagation:
                break

    def shutdown(self):
        self._executor.shutdown(wait=True)
