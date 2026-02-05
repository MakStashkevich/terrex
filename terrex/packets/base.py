from abc import ABC, abstractmethod
from typing import Type, Dict
from enum import Enum
from terrex.data.player import Player
from terrex.data.world import World
from terrex.events.eventmanager import EventManager
from terrex.util.streamer import Reader, Writer

registry: Dict[int, Type['Packet']] = {}

class Packet(ABC):
    id: int

    @classmethod
    def register(cls: Type['Packet']) -> Type['Packet']:
        registry[cls.id] = cls
        return cls

    def read(self, reader: Reader) -> None:
        raise NotImplementedError("Метод read должен быть переопределен")

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Метод write должен быть переопределен")

    def handle(self, world: World, player: Player, evman: EventManager) -> None:
        pass


class PacketDirection(Enum):
    CLIENT = "client"
    SERVER = "server"
    SYNC = "sync"


class ServerPacket(Packet):
    """Пакеты Server -> Client. Клиент только читает (read)."""
    _direction: PacketDirection = PacketDirection.SERVER

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        raise NotImplementedError(f"Клиент не отправляет {self.__class__.__name__} (пакет только от сервера)")

class ClientPacket(Packet):
    """Пакеты Client -> Server. Клиент только пишет (write)."""
    _direction: PacketDirection = PacketDirection.CLIENT

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass

    def read(self, reader: Reader) -> None:
        raise NotImplementedError(f"Клиент не читает {self.__class__.__name__} (пакет только к серверу)")

class SyncPacket(Packet):
    """Пакеты Server <-> Client (Sync). Оба метода."""
    _direction: PacketDirection = PacketDirection.SYNC

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass