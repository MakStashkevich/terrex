from dataclasses import dataclass

from terrex.packet.base import SyncPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class HitSwitch(SyncPacket):
    id = MessageID.HitSwitch

    def read(self, reader: Reader) -> None:
        self.x = reader.read_short()
        self.y = reader.read_short()

    def write(self, writer: Writer) -> None:
        writer.write_short(self.x)
        writer.write_short(self.y)
