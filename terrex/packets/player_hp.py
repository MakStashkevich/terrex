from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class PlayerHp(Packet):
    id = PacketIds.PLAYER_HP.value

    def __init__(self, player_id: int = 0, hp: int = 100, max_hp: int = 100):
        self.player_id = player_id
        self.hp = hp
        self.max_hp = max_hp

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.hp = reader.read_ushort()
        self.max_hp = reader.read_ushort()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_ushort(self.hp)
        writer.write_ushort(self.max_hp)

PlayerHp.register()