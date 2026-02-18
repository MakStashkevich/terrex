from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class ClientUUID(ClientPacket):
    id = MessageID.ClientUUID

    def __init__(self, uuid4: str = "01032c81-623f-4435-85e5-e0ec816b09ca"):
        self.uuid4 = uuid4

    def write(self, writer: Writer):
        writer.write_dotnet_string(self.uuid4)

    def read(self, reader: Reader) -> None:
        self.uuid4 = reader.read_dotnet_string()
