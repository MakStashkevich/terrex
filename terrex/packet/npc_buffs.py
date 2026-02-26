from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer

from .base import ServerPacket


class NPCBuffs(ServerPacket):
    id = MessageID.NPCBuffs
    MAX_BUFF = 20  # NPC.maxBuffs

    def __init__(self) -> None:
        self.npc_id: int = 0
        self.buffs: list[tuple[int, int]] = []  # (buff_type, buff_time)

    def read(self, reader: Reader) -> None:
        self.npc_id = reader.read_short()
        self.buffs = []
        while len(self.buffs) < self.MAX_BUFF:
            buff_type = reader.read_ushort()
            if buff_type == 0:  # packet every end on 0 ushort
                break  # packet ended
            time = reader.read_ushort()
            self.buffs.append((buff_type, time))

    # not used by client
    def write(self, writer: Writer) -> None:
        writer.write_short(self.npc_id)
        for buff_type, time in self.buffs:
            writer.write_ushort(buff_type)
            writer.write_ushort(time)
        writer.write_ushort(0)
