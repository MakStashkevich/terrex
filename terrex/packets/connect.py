from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class Connect(ClientPacket):
    id = PacketIds.CONNECT_REQUEST.value

    def __init__(self, version: int = 0):
        self.version = version

    def read(self, reader: Reader) -> None:
        version_str = reader.read_string()
        self.version = int(version_str.replace("Terraria", ""))

    def write(self, writer: Writer):
        writer.write_string("Terraria" + str(self.version))

Connect.register()