from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import ClientPacket


class ToggleParty(ClientPacket):
    id = MessageID.ToggleParty

    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        pass
