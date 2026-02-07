from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class HatRackSync(SyncPacket):
    id = PacketIds.TE_HAT_RACK_ITEM_SYNC.value

    def __init__(self, player_id: int = 0, tile_entity_id: int = 0, item_index: int = 0, item_id: int = 0, stack: int = 0, prefix: int = 0):
        self.player_id = player_id
        self.tile_entity_id = tile_entity_id
        self.item_index = item_index
        self.item_id = item_id
        self.stack = stack
        self.prefix = prefix

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.tile_entity_id = reader.read_int()
        self.item_index = reader.read_byte()
        self.item_id = reader.read_ushort()
        self.stack = reader.read_ushort()
        self.prefix = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_int(self.tile_entity_id)
        writer.write_byte(self.item_index)
        writer.write_ushort(self.item_id)
        writer.write_ushort(self.stack)
        writer.write_byte(self.prefix)


HatRackSync.register()
