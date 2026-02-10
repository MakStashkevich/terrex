from typing import Union
from abc import ABC, abstractmethod
from terrex.util.streamer import Reader, Writer


class NetServerModule(ABC):
    """
    Server -> Client
    """
    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("LoadNetServerPacket does not implement write")


class NetClientModule(ABC):
    """
    Client -> Server
    """
    def read(self, reader: Reader) -> None:
        raise NotImplementedError("LoadNetClientPacket does not implement read")

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass


class NetSyncModule(ABC):
    """
    Server <-> Client (Sync)
    """
    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass


NetModule = Union[NetServerModule, NetClientModule, NetSyncModule]