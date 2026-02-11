from typing import Any

from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class SendPassword(ClientPacket):
    id = PacketIds.SEND_PASSWORD

    def __init__(self, password: str = ""):
        self.password = password

    def write(self, writer: Writer):
        writer.write_dotnet_string(self.password)

    def read(self, reader: Reader) -> None:
        self.password = reader.read_dotnet_string()

SendPassword.register()