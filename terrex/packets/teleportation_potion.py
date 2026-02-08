from .packet_ids import PacketIds
from .base import SyncPacket
from ..util.streamer import Reader, Writer


class TeleportationPotion(SyncPacket):
    id = PacketIds.TELEPORTATION_POTION.value

    def __init__(self) -> None:
        self.packet_type: int = 0  # 0=TeleportationPotion, 1=MagicConch, 2=DemonConch

    def read(self, reader: Reader) -> None:
        self.packet_type = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.packet_type)

TeleportationPotion.register()