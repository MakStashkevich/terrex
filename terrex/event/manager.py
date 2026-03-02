import asyncio
import inspect
from collections.abc import Callable

from terrex.types import DecoratedHandler

from .dispatcher import Dispatcher
from .filter.base import EventFilter
from .types import BaseEvent
from typing import TypeVar

E = TypeVar("E", bound=BaseEvent)


class EventManager:
    def __init__(self, dispatcher: Dispatcher):
        self._dispatcher = dispatcher

    def on_event(self, filter: EventFilter[E]) -> Callable[[DecoratedHandler], DecoratedHandler]:
        def decorator(func: DecoratedHandler) -> DecoratedHandler:
            sig = inspect.signature(func)
            params = list(sig.parameters.values())
            if len(params) > 1:
                raise ValueError(
                    f"Обработчик события {func.__name__} должен иметь ровно один параметр: event"
                )

            if len(params) == 1:
                param = params[0]
                ann = param.annotation
                if ann is not inspect.Parameter.empty:
                    if not (inspect.isclass(ann) and issubclass(ann, BaseEvent)):
                        raise ValueError(
                            f"Аннотация события {ann} должна быть подклассом BaseEvent"
                        )

            self._dispatcher.register(filter, func)
            return func

        return decorator

    def raise_event(self, event: BaseEvent):
        loop = asyncio.get_running_loop()
        loop.create_task(self._dispatcher.dispatch(event))

    def stop(self):
        self._dispatcher.shutdown()
