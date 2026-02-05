from dataclasses import dataclass
from typing import Optional
from terrex.util.streamer import Reader, Writer

@dataclass
class Bestiary:
    variant: int  # 0: KillCount, 1: Sight, 2: Chat
    npc_net_id: int
    kill_count: Optional[int] = None

    @classmethod
    def read(cls, reader: Reader) -> 'Bestiary':
        variant = reader.read_byte()
        npc_net_id = reader.read_short()
        kill_count = reader.read_ushort() if variant == 0 else None
        return cls(variant, npc_net_id, kill_count)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.variant)
        writer.write_short(self.npc_net_id)
        if self.variant == 0:
            assert self.kill_count is not None
            writer.write_ushort(self.kill_count)