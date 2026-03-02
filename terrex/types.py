from collections.abc import Callable
from typing import Any, Awaitable, TypeVar

DecoratedHandler = TypeVar(
    "DecoratedHandler",
    bound=Callable[..., Awaitable[Any]]
)