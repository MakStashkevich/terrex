from typing import Optional
from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class UpdateNpcName(SyncPacket):
    id = PacketIds.UPDATE_NPC_NAME.value

    def __init__(self, npc_id: int = 0, name: Optional[str] = None, town_npc_variation_idx: Optional[int] = None):
        self.npc_id = npc_id
        self.name = name
        self.town_npc_variation_idx = town_npc_variation_idx

    def read(self, reader: Reader) -> None:
        self.npc_id = reader.read_short()
        if not reader.eof():
            self.name = reader.read_string()
            self.town_npc_variation_idx = reader.read_int()
        else:
            self.name = None
            self.town_npc_variation_idx = None

    def write(self, writer: Writer) -> None:
        writer.write_short(self.npc_id)
        if self.name is not None and self.town_npc_variation_idx is not None:
            writer.write_string(self.name)
            writer.write_int(self.town_npc_variation_idx)

UpdateNpcName.register()