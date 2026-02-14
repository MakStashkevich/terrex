from terrex.packets.base import Packet
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class Unknown15(Packet):
    id = MessageID.Unknown15

    def __init__(self, pkt_id: int = 0, version: str = ""):
        self.pkt_id = pkt_id
        self.version = version

    def read(self, reader: Reader) -> None:
        self.pkt_id = reader.read_short()
        self.version = reader.read_dotnet_string()

    def write(self, writer: Writer) -> None:
        writer.write_short(self.pkt_id)
        writer.write_dotnet_string(self.version)
