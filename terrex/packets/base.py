from abc import ABC, abstractmethod
from typing import Type, Dict
from terrex.util.streamer import Reader, Writer

registry: Dict[int, Type['Packet']] = {}

class Packet(ABC):
    id: int

    @classmethod
    def register(cls: Type['Packet']) -> Type['Packet']:
        registry[cls.id] = cls
        return cls

    @abstractmethod
    def read(self, reader: Reader) -> None:
        pass

    @abstractmethod
    def write(self, writer: Writer) -> None:
        pass

    def handle(self, world, player, evman) -> None:
        pass