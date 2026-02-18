from terrex.id import MessageID

from terrex.net.streamer import Reader, Writer
from .base import SyncPacket


class RequestTeleportationByServer(SyncPacket):
    id = MessageID.RequestTeleportationByServer

    def __init__(self) -> None:
        self.packet_type: int = 0  # 0=TeleportationPotion, 1=MagicConch, 2=DemonConch

    def read(self, reader: Reader) -> None:
        self.packet_type = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.packet_type)
