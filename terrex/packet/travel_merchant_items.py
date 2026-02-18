from terrex.id import MessageID

from terrex.net.streamer import Reader, Writer
from .base import ServerPacket


class TravelMerchantItems(ServerPacket):
    id = MessageID.TravelMerchantItems

    def __init__(self) -> None:
        self.items: list[int] = [0] * 40

    def read(self, reader: Reader) -> None:
        for i in range(40):
            self.items[i] = reader.read_short()

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Server does not send TravellingMerchantInventory (client-bound packet only)")
