from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer


class RequestTileEntityInteraction(SyncPacket):
    id = MessageID.RequestTileEntityInteraction

    def __init__(self, tile_entity_id: int = 0, player_id: int = 0):
        self.tile_entity_id = tile_entity_id
        self.player_id = player_id

    def read(self, reader: Reader):
        self.tile_entity_id = reader.read_int()
        self.player_id = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_int(self.tile_entity_id)
        writer.write_byte(self.player_id)



