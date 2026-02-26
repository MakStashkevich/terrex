from terrex.id import MessageID
from terrex.net.enum import TeleportRequestType
from terrex.net.streamer import Reader, Writer

from .base import SyncPacket


class RequestTeleportationByServer(SyncPacket):
    id = MessageID.RequestTeleportationByServer

    def __init__(self, type: TeleportRequestType = TeleportRequestType.TeleportationPotion) -> None:
        self.type: TeleportRequestType = type

    def read(self, reader: Reader) -> None:
        self.type = TeleportRequestType(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.type)
