from dataclasses import dataclass
from enum import IntEnum

from terrex.net.streamer import Reader, Writer

from .net_module import NetServerModule


class TagEffectMessageType(IntEnum):
    FullState = 0
    ChangeActiveEffect = 1
    ApplyTagToNPC = 2
    EnableProcOnNPC = 3
    ClearProcOnNPC = 4


@dataclass()
class NetTagEffectModule(NetServerModule):
    id: int = 12
    player_id: int | None = None
    msg_type: TagEffectMessageType | None = None
    effect_id: int | None = None
    npc_index: int | None = None
    time_left_sparse: list[tuple[int, int]] | None = None
    proc_time_sparse: list[tuple[int, int]] | None = None

    @classmethod
    def create(
        cls,
        player_id: int,
        msg_type: TagEffectMessageType,
        effect_id: int | None = None,
        npc_index: int | None = None,
        time_left_sparse: list[tuple[int, int]] | None = None,
        proc_time_sparse: list[tuple[int, int]] | None = None,
    ) -> "NetTagEffectModule":
        obj = cls()
        obj.player_id = player_id
        obj.msg_type = msg_type
        obj.effect_id = effect_id
        obj.npc_index = npc_index
        obj.time_left_sparse = time_left_sparse
        obj.proc_time_sparse = proc_time_sparse
        return obj

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.msg_type = TagEffectMessageType(reader.read_byte())
        self.effect_id = None
        self.npc_index = None
        self.time_left_sparse = None
        self.proc_time_sparse = None
        if self.msg_type == TagEffectMessageType.FullState:
            self.effect_id = reader.read_short()
            self.time_left_sparse = self._read_sparse(reader)
            self.proc_time_sparse = self._read_sparse(reader)
        elif self.msg_type == TagEffectMessageType.ChangeActiveEffect:
            self.effect_id = reader.read_short()
        elif self.msg_type in (TagEffectMessageType.ApplyTagToNPC, TagEffectMessageType.EnableProcOnNPC, TagEffectMessageType.ClearProcOnNPC):
            self.npc_index = reader.read_byte()

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
