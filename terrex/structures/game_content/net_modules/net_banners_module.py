from enum import IntEnum
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class BannersMessageType(IntEnum):
    FullState = 0
    KillCountUpdate = 1
    ClaimCountUpdate = 2
    ClaimRequest = 3
    ClaimResponse = 4


class NetBannersModule(NetServerModule):
    def __init__(
        self,
        msg_type: BannersMessageType,
        banner_id: int | None = None,
        kill_count: int | None = None,
        claimable_count: int | None = None,
        amount: int | None = None,
        granted: bool | None = None,
        kill_counts: list[int] | None = None,
        claimable_banners: list[int] | None = None,
    ):
        self.msg_type = msg_type
        self.banner_id = banner_id
        self.kill_count = kill_count
        self.claimable_count = claimable_count
        self.amount = amount
        self.granted = granted
        self.kill_counts = kill_counts
        self.claimable_banners = claimable_banners

    @classmethod
    def read(cls, reader: Reader) -> 'NetBannersModule':
        msg_type = BannersMessageType(reader.read_byte())
        banner_id = None
        kill_count = None
        claimable_count = None
        amount = None
        granted = None

        kill_counts = None
        claimable_banners = None
        if msg_type == BannersMessageType.FullState:
            num = reader.read_short()
            kill_counts = [reader.read_int() for _ in range(num)]
            claimable_banners = None
            if reader.version >= 289:
                num_claim = reader.read_short()
                claimable_banners = [reader.read_ushort() for _ in range(num_claim)]
        elif msg_type == BannersMessageType.KillCountUpdate:
            banner_id = reader.read_short()
            kill_count = reader.read_int()
        elif msg_type == BannersMessageType.ClaimCountUpdate:
            banner_id = reader.read_short()
            claimable_count = reader.read_ushort()
        elif msg_type == BannersMessageType.ClaimRequest:
            banner_id = reader.read_short()
            amount = reader.read_ushort()
        elif msg_type == BannersMessageType.ClaimResponse:
            banner_id = reader.read_short()
            amount = reader.read_ushort()
            granted = reader.read_bool()

        return cls(
            msg_type,
            banner_id=banner_id,
            kill_count=kill_count,
            claimable_count=claimable_count,
            amount=amount,
            granted=granted,
            kill_counts=kill_counts,
            claimable_banners=claimable_banners,
        )

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
