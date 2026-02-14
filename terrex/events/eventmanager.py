from collections.abc import Callable
from typing import Any

from terrex.events.events import Event


class EventManager:

    def __init__(self):
        self.event_listeners = {}
        self.event_methods = {}

    """A decorator function
        Use it as follows:

        eventmanager = bot.get_event_manager()

        @eventmanager.on_event(Events.CHAT)
        def chat_message(self, data):
            print(data)

    """

    def on_event(self, event_id: Event):
        def add_wrapper(f: Callable[[Any], None]):
            if event_id not in self.event_listeners:
                self.event_listeners[event_id] = []
            if callable(f):
                self.event_listeners[event_id].append(f)
            return f

        return add_wrapper

    def method_on_event(self, event_id: Event, listener: Callable[[Any], None]):
        if event_id not in self.event_methods:
            self.event_methods[event_id] = []
        if callable(listener):
            self.event_methods[event_id].append(listener)

    def raise_event(self, event_id: Event, data: Any):
        # print("Event happened: ", event_id)
        if event_id in self.event_listeners:
            for f in self.event_listeners[event_id]:
                f(data)
        if event_id in self.event_methods:
            for f in self.event_methods[event_id]:
                if callable(f):
                    f(data)
