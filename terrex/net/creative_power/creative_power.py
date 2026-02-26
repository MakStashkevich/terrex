import inspect
from abc import ABC, abstractmethod
from typing import Any

from terrex.net.streamer import Reader, Writer
from terrex.util.stringify import stringify_value

creative_power_registry: dict[int, type["CreativePower"]] = {}


class CreativePower(ABC):
    id: int

    def __init_subclass__(cls):
        super().__init_subclass__()

        if inspect.isabstract(cls):
            return

        if not hasattr(cls, "id"):
            raise TypeError(f"{cls.__name__} must define class attribute 'id'")

        if "create" not in cls.__dict__:
            raise TypeError(f"{cls.__name__} must implement classmethod create()")

        if cls.id in creative_power_registry:
            raise ValueError(
                f"CreativePower id {cls.id} already registered for {creative_power_registry[cls.id]}"
            )
        creative_power_registry[cls.id] = cls

    def __to_log_dict(self) -> dict[str, Any]:
        return {name: stringify_value(value) for name, value in vars(self).items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__to_log_dict()})"

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass
