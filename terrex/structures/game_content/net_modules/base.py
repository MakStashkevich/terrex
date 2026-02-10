from typing import Any, Union
from abc import ABC, abstractmethod
from dataclasses import is_dataclass
from terrex.util.streamer import Reader, Writer
from terrex.util.stringify import stringify_value


class NetModule(ABC):
    def __to_log_dict(self) -> dict[str, Any]:
        return {name: stringify_value(value) for name, value in vars(self).items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__to_log_dict()})"


class NetServerModule(NetModule, ABC):
    """
    Server -> Client
    """
    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("NetServerModule does not implement write")


class NetClientModule(NetModule, ABC):
    """
    Client -> Server
    """
    def read(self, reader: Reader) -> None:
        raise NotImplementedError("NetClientModule does not implement read")

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass


class NetSyncModule(NetModule, ABC):
    """
    Server <-> Client (Sync)
    """
    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass


NetModuleType = Union[NetServerModule, NetClientModule, NetSyncModule]
