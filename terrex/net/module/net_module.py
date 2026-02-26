import inspect
from abc import ABC, abstractmethod
from typing import Any

from terrex.net.streamer import Reader, Writer
from terrex.util.stringify import stringify_value

net_module_registry: dict[int, type["NetModule"]] = {}


class NetModule(ABC):
    id: int

    def __init_subclass__(cls):
        super().__init_subclass__()

        if inspect.isabstract(cls):
            return

        if not hasattr(cls, "id"):
            raise TypeError(f"{cls.__name__} must define class attribute 'id'")

        if "create" not in cls.__dict__:
            raise TypeError(f"{cls.__name__} must implement classmethod create()")

        if cls.id in net_module_registry:
            raise ValueError(
                f"Module id {cls.id} already registered for {net_module_registry[cls.id]}"
            )
        net_module_registry[cls.id] = cls

    def __to_log_dict(self) -> dict[str, Any]:
        return {name: stringify_value(value) for name, value in vars(self).items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__to_log_dict()})"

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError(f"create() not implemented in {cls.__class__.__name__}")

    @abstractmethod
    def read(self, reader: Reader) -> None:
        raise NotImplementedError(f"read() not implemented in {self.__class__.__name__}")

    @abstractmethod
    def write(self, writer: Writer) -> None:
        raise NotImplementedError(f"_write() not implemented in {self.__class__.__name__}")


class NetServerModule(NetModule, ABC):
    """
    Server -> Client
    """


class NetClientModule(NetModule, ABC):
    """
    Client -> Server
    """


class NetSyncModule(NetModule, ABC):
    """
    Server <-> Client (Sync)
    """
