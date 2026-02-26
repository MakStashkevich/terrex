from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer
from terrex.packet.base import SyncPacket


class UniqueTownNPCInfoSyncRequest(SyncPacket):
    id = MessageID.UniqueTownNPCInfoSyncRequest

    def __init__(
        self, npc_id: int = 0, name: str | None = None, town_npc_variation_idx: int | None = None
    ):
        self.npc_id = npc_id
        self.name = name
        self.town_npc_variation_idx = town_npc_variation_idx

    def read(self, reader: Reader) -> None:
        self.npc_id = reader.read_short()
        if not reader.eof():
            self.name = reader.read_dotnet_string()
            self.town_npc_variation_idx = reader.read_int()
        else:
            self.name = None
            self.town_npc_variation_idx = None

    def write(self, writer: Writer) -> None:
        writer.write_short(self.npc_id)
        if self.name is not None and self.town_npc_variation_idx is not None:
            writer.write_dotnet_string(self.name)
            writer.write_int(self.town_npc_variation_idx)
