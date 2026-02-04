from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class Connect(Packet):
    id = PacketIds.CONNECT_REQUEST.value

    def __init__(self, version: str = "Terraria238"):
        self.version = version

    def read(self, reader: Reader):
        self.version = reader.read_string()

    def write(self, writer: Writer):
        writer.write_string(self.version)

Connect.register()