from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class LoadoutPlayerUpdate(ClientPacket):
    id = PacketIds.LOADOUT_PLAYER_UPDATE.value

    def __init__(self, target_id: int = 0, loadout_index: int = 0, accessory_visibility: int = 0):
        self.target_id = target_id
        self.loadout_index = loadout_index
        self.accessory_visibility = accessory_visibility

    def read(self, reader: Reader):
        self.target_id = reader.read_byte()
        self.loadout_index = reader.read_byte()
        self.accessory_visibility = reader.read_ushort()

    def write(self, writer: Writer):
        writer.write_byte(self.target_id)
        writer.write_byte(self.loadout_index)
        writer.write_ushort(self.accessory_visibility)


LoadoutPlayerUpdate.register()