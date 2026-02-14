from terrex.packets.base import ClientPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class Hello(ClientPacket):
    id = MessageID.Hello

    def __init__(self, version: int = 0):
        self.version = version

    def read(self, reader: Reader) -> None:
        version_str = reader.read_dotnet_string()
        self.version = int(version_str.replace("Terraria", ""))

    def write(self, writer: Writer):
        writer.write_dotnet_string("Terraria" + str(self.version))
