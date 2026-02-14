from terrex.packets.base import ServerPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class DevCommands(ServerPacket):
    id = MessageID.DevCommands

    def __init__(self, buf: bytes = b""):
        self.buf = buf

    def read(self, reader: Reader):
        self.buf = reader.remaining()

    def write(self, writer: Writer):
        writer.write_bytes(self.buf)
