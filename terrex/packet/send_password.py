from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import ClientPacket


class SendPassword(ClientPacket):
    id = MessageID.SendPassword

    def __init__(self, password: str = ""):
        self.password = password

    def write(self, writer: Writer):
        writer.write_dotnet_string(self.password)

    def read(self, reader: Reader) -> None:
        self.password = reader.read_dotnet_string()
