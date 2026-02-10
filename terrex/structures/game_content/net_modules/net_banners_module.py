from dataclasses import dataclass
from enum import IntEnum
from typing import List
from terrex.util.streamer import Reader, Writer
from .net_module import NetServerModule

class BannersMessageType(IntEnum):
    FullState = 0
    KillCountUpdate = 1
    ClaimCountUpdate = 2
    ClaimRequest = 3
    ClaimResponse = 4

@dataclass()
class NetBannersModule(NetServerModule):
    id: int = 10
    msg_type: BannersMessageType | None = None
    banner_id: int | None = None
    kill_count: int | None = None
    claimable_count: int | None = None
    amount: int | None = None
    granted: bool | None = None
    kill_counts: List[int] | None = None
    claimable_banners: List[int] | None = None

    @classmethod
    def create(
        cls,
        msg_type: BannersMessageType,
        banner_id: int | None = None,
        kill_count: int | None = None,
        claimable_count: int | None = None,
        amount: int | None = None,
        granted: bool | None = None,
        kill_counts: List[int] | None = None,
        claimable_banners: List[int] | None = None,
    ) -> 'NetBannersModule':
        obj = cls()
        obj.msg_type = msg_type
        obj.banner_id = banner_id
        obj.kill_count = kill_count
        obj.claimable_count = claimable_count
        obj.amount = amount
        obj.granted = granted
        obj.kill_counts = kill_counts
        obj.claimable_banners = claimable_banners
        return obj

    def read(self, reader: Reader) -> None:
        self.msg_type = BannersMessageType(reader.read_byte())
        self.banner_id = None
        self.kill_count = None
        self.claimable_count = None
        self.amount = None
        self.granted = None
        self.kill_counts = None
        self.claimable_banners = None
        if self.msg_type == BannersMessageType.FullState:
            num = reader.read_short()
            self.kill_counts = [reader.read_int() for _ in range(num)]
            if reader.version >= 289:
                num_claim = reader.read_short()
                self.claimable_banners = [reader.read_ushort() for _ in range(num_claim)]
        elif self.msg_type == BannersMessageType.KillCountUpdate:
            self.banner_id = reader.read_short()
            self.kill_count = reader.read_int()
        elif self.msg_type == BannersMessageType.ClaimCountUpdate:
            self.banner_id = reader.read_short()
            self.claimable_count = reader.read_ushort()
        elif self.msg_type == BannersMessageType.ClaimRequest:
            self.banner_id = reader.read_short()
            self.amount = reader.read_ushort()
        elif self.msg_type == BannersMessageType.ClaimResponse:
            self.banner_id = reader.read_short()
            self.amount = reader.read_ushort()
            self.granted = reader.read_bool()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.msg_type.value)
        if self.msg_type == BannersMessageType.FullState:
            if self.kill_counts is not None:
                writer.write_short(len(self.kill_counts))
                for kc in self.kill_counts:
                    writer.write_int(kc)
            if self.claimable_banners is not None:
                writer.write_short(len(self.claimable_banners))
                for cb in self.claimable_banners:
                    writer.write_ushort(cb)
        elif self.msg_type == BannersMessageType.KillCountUpdate:
            writer.write_short(self.banner_id)
            writer.write_int(self.kill_count)
        elif self.msg_type == BannersMessageType.ClaimCountUpdate:
            writer.write_short(self.banner_id)
            writer.write_ushort(self.claimable_count)
        elif self.msg_type == BannersMessageType.ClaimRequest:
            writer.write_short(self.banner_id)
            writer.write_ushort(self.amount)
        elif self.msg_type == BannersMessageType.ClaimResponse:
            writer.write_short(self.banner_id)
            writer.write_ushort(self.amount)
            writer.write_bool(self.granted)
