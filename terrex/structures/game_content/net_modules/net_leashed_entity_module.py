from enum import IntEnum
from typing import Tuple
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class LeashedEntityMessageType(IntEnum):
    Remove = 0
    FullSync = 1
    PartialSync = 2


class NetLeashedEntityModule(NetServerModule):
    def __init__(
        self,
        msg_type: LeashedEntityMessageType,
        slot: int,
        leashed_type: int | None = None,
        anchor: tuple[int, int] | None = None,
        extra_data: bytes = b"",
    ):
        self.msg_type = msg_type
        self.slot = slot
        self.leashed_type = leashed_type
        self.anchor = anchor
        self.extra_data = extra_data

    @classmethod
    def read(cls, reader: Reader) -> 'NetLeashedEntityModule':
        msg_type = LeashedEntityMessageType(reader.read_byte())
        slot = reader.read_7bit_encoded_int()
        leashed_type = None
        anchor = None
        extra_data = b""
        if msg_type in (LeashedEntityMessageType.FullSync, LeashedEntityMessageType.PartialSync):
            leashed_type = reader.read_7bit_encoded_int()
            if msg_type == LeashedEntityMessageType.FullSync:
                anchor_x = reader.read_short()
                anchor_y = reader.read_short()
                anchor = (anchor_x, anchor_y)
        remaining_len = len(reader.remaining())
        extra_data = reader.read_bytes(remaining_len)
        return cls(msg_type, slot, leashed_type, anchor, extra_data)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.msg_type.value)
        writer.write_7bit_encoded_int(self.slot)
        if self.msg_type in (LeashedEntityMessageType.FullSync, LeashedEntityMessageType.PartialSync):
            writer.write_7bit_encoded_int(self.leashed_type)
            if self.msg_type == LeashedEntityMessageType.FullSync:
                writer.write_short(self.anchor[0])
                writer.write_short(self.anchor[1])
        writer.write_bytes(self.extra_data)
