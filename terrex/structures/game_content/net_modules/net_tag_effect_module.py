from enum import IntEnum
from typing import List, Tuple
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class TagEffectMessageType(IntEnum):
    FullState = 0
    ChangeActiveEffect = 1
    ApplyTagToNPC = 2
    EnableProcOnNPC = 3
    ClearProcOnNPC = 4


class NetTagEffectModule(NetServerModule):
    def __init__(
        self,
        player_id: int,
        msg_type: TagEffectMessageType,
        effect_id: int | None = None,
        npc_index: int | None = None,
        time_left_sparse: list[tuple[int, int]] | None = None,
        proc_time_sparse: list[tuple[int, int]] | None = None,
    ):
        self.player_id = player_id
        self.msg_type = msg_type
        self.effect_id = effect_id
        self.npc_index = npc_index
        self.time_left_sparse = time_left_sparse
        self.proc_time_sparse = proc_time_sparse

    @classmethod
    def read(cls, reader: Reader) -> 'NetTagEffectModule':
        player_id = reader.read_byte()
        msg_type = TagEffectMessageType(reader.read_byte())
        effect_id = None
        npc_index = None
        time_left_sparse = None
        proc_time_sparse = None
        if msg_type == TagEffectMessageType.FullState:
            effect_id = reader.read_short()
            time_left_sparse = cls._read_sparse(reader)
            proc_time_sparse = cls._read_sparse(reader)
        elif msg_type == TagEffectMessageType.ChangeActiveEffect:
            effect_id = reader.read_short()
        elif msg_type in (TagEffectMessageType.ApplyTagToNPC, TagEffectMessageType.EnableProcOnNPC, TagEffectMessageType.ClearProcOnNPC):
            npc_index = reader.read_byte()
        return cls(player_id, msg_type, effect_id, npc_index, time_left_sparse, proc_time_sparse)

    @classmethod
    def _read_sparse(cls, reader: Reader) -> list[tuple[int, int]]:
        sparse = []
        while True:
            idx = reader.read_byte()
            if idx >= 255:
                break
            time = reader.read_int()
            sparse.append((idx, time))
        return sparse

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_byte(self.msg_type.value)
        if self.msg_type == TagEffectMessageType.FullState:
            writer.write_short(self.effect_id)
            self._write_sparse(writer, self.time_left_sparse or [])
            self._write_sparse(writer, self.proc_time_sparse or [])
        elif self.msg_type == TagEffectMessageType.ChangeActiveEffect:
            writer.write_short(self.effect_id)
        elif self.msg_type in (TagEffectMessageType.ApplyTagToNPC, TagEffectMessageType.EnableProcOnNPC, TagEffectMessageType.ClearProcOnNPC):
            writer.write_byte(self.npc_index)

    def _write_sparse(self, writer: Writer, sparse: list[tuple[int, int]]) -> None:
        for idx, time in sparse:
            writer.write_byte(idx)
            writer.write_int(time)
        writer.write_byte(255)
