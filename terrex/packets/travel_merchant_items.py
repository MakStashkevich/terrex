from typing import List
from terrex.structures.id import MessageID
from .base import ServerPacket
from ..util.streamer import Reader, Writer


class TravelMerchantItems(ServerPacket):
    id = MessageID.TravelMerchantItems

    def __init__(self) -> None:
        self.items: List[int] = [0] * 40

    def read(self, reader: Reader) -> None:
        for i in range(40):
            self.items[i] = reader.read_short()

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Server does not send TravellingMerchantInventory (client-bound packet only)")

