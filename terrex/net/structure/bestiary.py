from dataclasses import dataclass
from enum import IntEnum

from terrex.net.streamer import Reader, Writer


class BestiaryUnlockType(IntEnum):
    Kill = 0
    Sight = 1
    Chat = 2


@dataclass
class Bestiary:
    unlock_type: BestiaryUnlockType
    npc_net_id: int
    kill_count: int | None = None

    @classmethod
    def read(cls, reader: Reader) -> 'Bestiary':
        unlock_type = BestiaryUnlockType(reader.read_byte())
        npc_net_id = reader.read_short()
        kill_count = (
            reader.read_7bit_encoded_int() if unlock_type == BestiaryUnlockType.Kill else None
        )
        return cls(unlock_type, npc_net_id, kill_count)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.unlock_type.value)
        writer.write_short(self.npc_net_id)
        if self.unlock_type == BestiaryUnlockType.Kill:
            assert self.kill_count is not None
            writer.write_7bit_encoded_int(self.kill_count)
