from abc import ABC, abstractmethod
from dataclasses import is_dataclass
from typing import Any, Type, Dict
from enum import Enum
from terrex.data.player import Player
from terrex.data.world import World
from terrex.events.eventmanager import EventManager
from terrex.util.streamer import Reader, Writer
from terrex.util.stringify import stringify_value

registry: Dict[int, Type['Packet']] = {}


class Packet(ABC):
    id: int

    @classmethod
    def register(cls: Type['Packet']) -> Type['Packet']:
        registry[cls.id] = cls
        return cls

    def read(self, reader: Reader) -> None:
        raise NotImplementedError("Method read must be overridden")

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Method write must be overridden")

    def handle(self, world: World, player: Player, evman: EventManager) -> None:
        pass
    
    def __to_log_dict(self) -> dict[str, Any]:
        return {name: stringify_value(value) for name, value in vars(self).items()}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__to_log_dict()})"


class PacketDirection(Enum):
    CLIENT = "client"
    SERVER = "server"
    SYNC = "sync"


class ServerPacket(Packet):
    """Server -> Client packets. Client only reads (read)."""
    _direction: PacketDirection = PacketDirection.SERVER

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        raise NotImplementedError(f"Client does not send {self.__class__.__name__} (server-only packet)")

class ClientPacket(Packet):
    """Client -> Server packets. Client only writes (write)."""
    _direction: PacketDirection = PacketDirection.CLIENT

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass

    def read(self, reader: Reader) -> None:
        raise NotImplementedError(f"Client does not read {self.__class__.__name__} (server-bound packet only)")

class SyncPacket(Packet):
    """Server <-> Client (Sync) packets. Both methods required."""
    _direction: PacketDirection = PacketDirection.SYNC

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass
