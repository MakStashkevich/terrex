from collections.abc import Callable
from typing import Any
import asyncio
import concurrent.futures
import inspect

from terrex.event.event import Event


class EventManager:

    def __init__(self):
        self.event_listeners = {}
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    def on_event(self, event_id: Event):
        """
        Decorator to register a function as an event listener for event_id.

        Usage:
        terrex = Terrex()
        evman = terrex.get_event_manager()

        Sync example:
        @evman.on_event(Event.CHAT)
        def handler(data):
            print(data)

        Async example:
        @evman.on_event(Event.CHAT)
        async def async_handler(data):
            await asyncio.sleep(1)
            print(data)

        Both sync and async functions are supported.
        """

        def add_wrapper(f: Callable[[Any], None]):
            if event_id not in self.event_listeners:
                self.event_listeners[event_id] = []
            self.event_listeners[event_id].append(f)
            return f

        return add_wrapper

    def method_on_event(self, event_id: Event, listener: Callable[[Any], None]):
        """
        Registers a callable as an event listener for event_id.

        Usage:
        terrex = Terrex()
        evman = terrex.get_event_manager()

        Sync example:
        evman.method_on_event(Event.CHAT, self.handler)

        def handler(self, data):
            print(data)

        Async example:
        evman.method_on_event(Event.CHAT, self.async_handler)

        async def async_handler(self, data):
            await asyncio.sleep(1)
            print(data)

        Supports sync and async callables.
        """
        if event_id not in self.event_listeners:
            self.event_listeners[event_id] = []
        self.event_listeners[event_id].append(listener)

    async def raise_event(self, event_id: Event, data: Any = None):
        handlers = self.event_listeners.get(event_id, [])
        coros = []
        loop = asyncio.get_running_loop()

        for f in handlers:
            if inspect.iscoroutinefunction(f):
                # every async func execute on current event loop
                coros.append(f(data))
            else:
                # every sync func execute on thread executor
                coros.append(loop.run_in_executor(self.executor, f, data))

        if coros:
            await asyncio.gather(*coros, return_exceptions=True)
