from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class SetUserSlot(Packet):
    id = PacketIds.SET_USER_SLOT.value

    def __init__(self, player_id: int = 0, is_server: bool = False):
        self.player_id = player_id
        self.is_server = is_server

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.is_server = reader.read_bool()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_bool(self.is_server)

SetUserSlot.register()