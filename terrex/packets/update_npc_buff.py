from typing import List, Tuple
from .packet_ids import PacketIds
from .base import ServerPacket
from ..util.streamer import Reader, Writer


class UpdateNpcBuff(ServerPacket):
    id = PacketIds.UPDATE_NPC_BUFF.value

    def __init__(self) -> None:
        self.npc_id: int = 0
        self.buffs: List[Tuple[int, int]] = [(0, 0)] * 5  # (buff_id, time)

    def read(self, reader: Reader) -> None:
        self.npc_id = reader.read_short()
        self.buffs = []
        for _ in range(5):
            buff_id = reader.read_ushort()
            time = reader.read_short()
            self.buffs.append((buff_id, time))

    def write(self, writer: Writer) -> None:
        raise NotImplementedError("Server does not send UpdateNpcBuff (client-bound packet only)")

UpdateNpcBuff.register()