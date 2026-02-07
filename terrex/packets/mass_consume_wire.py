from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class MassConsumeWire(ServerPacket):
    id = PacketIds.MASS_WIRE_OPERATION_CONSUME.value

    def __init__(self, item_type: int = 0, quantity: int = 0, player_id: int = 0):
        self.item_type = item_type
        self.quantity = quantity
        self.player_id = player_id

    def read(self, reader: Reader):
        self.item_type = reader.read_short()
        self.quantity = reader.read_short()
        self.player_id = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_short(self.item_type)
        writer.write_short(self.quantity)
        writer.write_byte(self.player_id)


MassConsumeWire.register()
