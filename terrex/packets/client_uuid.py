from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class ClientUuid(Packet):
    id = PacketIds.CLIENT_UUID.value

    def __init__(self, uuid4: str = "01032c81-623f-4435-85e5-e0ec816b09ca"):
        self.uuid4 = uuid4

    def read(self, reader: Reader):
        self.uuid4 = reader.read_string()

    def write(self, writer: Writer):
        writer.write_string(self.uuid4)

ClientUuid.register()