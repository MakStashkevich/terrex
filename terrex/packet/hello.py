from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import ClientPacket


class Hello(ClientPacket):
    """
    It is used for the first request and comparison by the server of the Terraria version with the client version.

    In case of an error, the server sends a Kick [2] packet and terminates the connection.
    """

    id = MessageID.Hello

    def __init__(self, version: int = 0):
        self.version = version

    def read(self, reader: Reader) -> None:
        version_str = reader.read_dotnet_string()
        self.version = int(version_str.replace("Terraria", ""))

    def write(self, writer: Writer):
        writer.write_dotnet_string("Terraria" + str(self.version))
