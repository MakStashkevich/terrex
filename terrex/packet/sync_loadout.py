from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import ClientPacket


class SyncLoadout(ClientPacket):
    id = MessageID.SyncLoadout

    def __init__(self, player_id: int = 0, loadout_index: int = 0, accessory_visibility: int = 0):
        self.player_id = player_id
        self.loadout_index = loadout_index
        self.accessory_visibility = accessory_visibility

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.loadout_index = reader.read_byte()
        self.accessory_visibility = reader.read_ushort()

    async def handle(self, world, player, evman):
        if not self.player_id in world.players:
            return
        current_player = world.players[self.player_id]
        current_player.loadout_index = self.loadout_index
        current_player.accessory_visibility = self.accessory_visibility

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.loadout_index)
        writer.write_ushort(self.accessory_visibility)
