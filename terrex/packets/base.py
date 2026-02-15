import inspect
from abc import ABC, abstractmethod
from typing import Any

from terrex.entity.player import Player
from terrex.events.eventmanager import EventManager
from terrex.structures.net_mode import NetMode
from terrex.util.streamer import Reader, Writer
from terrex.util.stringify import stringify_value
from terrex.world.world import World

packet_registry: dict[int, type["Packet"]] = {}


class Packet(ABC):
    id: int

    def read(self, reader: Reader) -> None:
        raise NotImplementedError("Method read must be overridden")

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Method write must be overridden")

    def handle(self, world: World, player: Player, evman: EventManager) -> None:
        """Optional method to handle the packet"""
        raise NotImplementedError("Method handle can be overridden if needed")

    def __init_subclass__(cls):
        super().__init_subclass__()

        if inspect.isabstract(cls):
            return

        if not isinstance(getattr(cls, "id", None), int):
            raise TypeError(f"{cls.__name__} must define class attribute 'id'")

        if not callable(getattr(cls, "read", None)):
            raise TypeError(f"{cls.__name__} must implement read()")

        if cls.id in packet_registry:
            raise ValueError(f"Packet id {cls.id} already registered for {packet_registry[cls.id]}")

        packet_registry[cls.id] = cls

    def __to_log_dict(self) -> dict[str, Any]:
        return {name: stringify_value(value) for name, value in vars(self).items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__to_log_dict()})"


class ServerPacket(Packet, ABC):
    """Server -> Client packets. Client only reads (read)."""

    _net_mode: NetMode = NetMode.SERVER

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        raise NotImplementedError(f"Client does not send {self.__class__.__name__} (server-only packet)")


class ClientPacket(Packet, ABC):
    """Client -> Server packets. Client only writes (write)."""

    _net_mode: NetMode = NetMode.CLIENT

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass

    def read(self, reader: Reader) -> None:
        raise NotImplementedError(f"Client does not read {self.__class__.__name__} (server-bound packet only)")


class SyncPacket(Packet, ABC):
    """Server <-> Client (Sync) packets. Both methods required."""

    _net_mode: NetMode = NetMode.SYNC

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass
