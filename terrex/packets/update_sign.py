from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class UpdateSign(Packet):
    id = PacketIds.UPDATE_SIGN.value

    def __init__(self, sign_id: int = 0, x: int = 0, y: int = 0, text: str = "", player_id: int = 0, flags: int = 0):
        self.sign_id = sign_id
        self.x = x
        self.y = y
        self.text = text
        self.player_id = player_id
        self.flags = flags

    def read(self, reader: Reader):
        self.sign_id = reader.read_short()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.text = reader.read_string()
        self.player_id = reader.read_byte()
        self.flags = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.sign_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_string(self.text)
        writer.write_byte(self.player_id)
        writer.write_byte(self.flags)

UpdateSign.register()