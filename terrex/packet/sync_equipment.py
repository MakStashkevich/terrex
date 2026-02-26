from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class SyncEquipment(SyncPacket):
    id = MessageID.SyncEquipment

    # 0 - 49 = Inventory
    # 50 - 53 = Money
    # 54 - 57 = Ammunition
    # 58 = Cursor
    # 59 - 61 = Armor
    # 62 - 67 = Acsesuars
    # 68 ???
    # 69 - 71 = Armor decorations
    # 72 - 77 = Acsesuars decorations
    # 78 ???
    # 79 - 87 = Dye (красители)
    # 88 ???
    # 89 - 93 MiscEquips (обычный питомец, светящийся питомец, вагонетка, ездовой питомец, крюк)
    # 94 - 98 = MiscDyes (красители животных)
    # 99 - 138 = Piggy bank
    # 499 = Trash

    # not tested
    # 139 - 178 = Safe
    # 180 - 219 = Defender's Forge
    # 220 - 259 = Void Vault
    def __init__(
        self,
        player_id: int = 0,
        slot_id: int = 0,
        stack: int = 0,
        prefix: int = 0,
        item_netid: int = 0,
    ):
        self.player_id = player_id
        self.slot_id = slot_id
        self.stack = stack
        self.prefix = prefix
        self.item_netid = item_netid

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.slot_id = reader.read_short()
        self.stack = reader.read_short()
        self.prefix = reader.read_byte()
        self.item_netid = reader.read_ushort()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_short(self.slot_id)
        writer.write_short(self.stack)
        writer.write_byte(self.prefix)
        writer.write_ushort(self.item_netid)
