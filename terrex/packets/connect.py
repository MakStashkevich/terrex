from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Writer

class Connect(ClientPacket):
    id = PacketIds.CONNECT_REQUEST.value

    def __init__(self, version: str = "Terraria238"):
        self.version = version

    def write(self, writer: Writer):
        writer.write_string(self.version)

Connect.register()