from terrex.packet.base import ServerPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class DevCommands(ServerPacket):
    id = MessageID.DevCommands

    def __init__(self, buf: bytes = b""):
        self.buf = buf

    def read(self, reader: Reader):
        self.buf = reader.remaining()

    def write(self, writer: Writer):
        writer.write_bytes(self.buf)
