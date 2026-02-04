from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class SendPassword(Packet):
    id = PacketIds.SEND_PASSWORD.value

    def __init__(self, password: str = ""):
        self.password = password

    def read(self, reader: Reader):
        self.password = reader.read_string()

    def write(self, writer: Writer):
        writer.write_string(self.password)

SendPassword.register()