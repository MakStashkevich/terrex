from dataclasses import dataclass
from enum import IntEnum

from terrex.net.streamer import Reader, Writer

from .net_module import NetServerModule


class LeashedEntityMessageType(IntEnum):
    Remove = 0
    FullSync = 1
    PartialSync = 2


@dataclass()
class NetLeashedEntityModule(NetServerModule):
    id: int = 13
    msg_type: LeashedEntityMessageType | None = None
    slot: int | None = None
    leashed_type: int | None = None
    anchor: tuple[int, int] | None = None
    extra_data: bytes | None = None

    @classmethod
    def create(
        cls,
        msg_type: LeashedEntityMessageType,
        slot: int,
        leashed_type: int | None = None,
        anchor: tuple[int, int] | None = None,
        extra_data: bytes | None = None,
    ) -> "NetLeashedEntityModule":
        obj = cls()
        obj.msg_type = msg_type
        obj.slot = slot
        obj.leashed_type = leashed_type
        obj.anchor = anchor
        obj.extra_data = extra_data
        return obj

    def read(self, reader: Reader) -> None:
        self.msg_type = LeashedEntityMessageType(reader.read_byte())
        self.slot = reader.read_7bit_encoded_int()
        self.leashed_type = None
        self.anchor = None
        self.extra_data = b""
        if self.msg_type in (
            LeashedEntityMessageType.FullSync,
            LeashedEntityMessageType.PartialSync,
        ):
            self.leashed_type = reader.read_7bit_encoded_int()
            if self.msg_type == LeashedEntityMessageType.FullSync:
                anchor_x = reader.read_short()
                anchor_y = reader.read_short()
                self.anchor = (anchor_x, anchor_y)
        remaining_len = len(reader.remaining())
        self.extra_data = reader.read_bytes(remaining_len)

    def write(self, writer: Writer) -> None:
        if self.msg_type is None or self.slot is None:
            raise ValueError("msg_type and slot must not be None")
        writer.write_byte(self.msg_type.value)
        writer.write_7bit_encoded_int(self.slot)
        if self.msg_type in (
            LeashedEntityMessageType.FullSync,
            LeashedEntityMessageType.PartialSync,
        ):
            if self.leashed_type is None:
                raise ValueError("leashed_type must not be None for FullSync/PartialSync")
            writer.write_7bit_encoded_int(self.leashed_type)
            if self.msg_type == LeashedEntityMessageType.FullSync:
                if self.anchor is None:
                    raise ValueError("anchor must not be None for FullSync")
                writer.write_short(self.anchor[0])
                writer.write_short(self.anchor[1])
        if self.extra_data is None:
            raise ValueError("extra_data must not be None")
        writer.write_bytes(self.extra_data)
