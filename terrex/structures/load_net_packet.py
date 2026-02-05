from typing import Union
from abc import ABC

from terrex.packets.base import ServerPacket, ClientPacket, SyncPacket


class LoadNetServerPacket(ServerPacket, ABC):
    """
    Server -> Client
    """
    pass


class LoadNetClientPacket(ClientPacket, ABC):
    """
    Client -> Server
    """
    pass


class LoadNetSyncPacket(SyncPacket, ABC):
    """
    Server <-> Client (Sync)
    """
    pass


LoadNetPacket = Union[LoadNetServerPacket, LoadNetClientPacket, LoadNetSyncPacket]