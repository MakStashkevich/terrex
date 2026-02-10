from typing import List
from terrex.structures.game_content.ambience.sky_entity_type import SkyEntityType
from terrex.structures.game_content.drawing.particle_orchestra_settings import ParticleOrchestraSettings
from terrex.structures.game_content.teleport_pylon_type import TeleportPylonType
from terrex.util.streamer import Reader, Writer
from terrex.structures.game_content.liquid import Liquid
from terrex.structures.game_content.bestiary import Bestiary
from terrex.structures.game_content.creative.creative_power import CreativePower
from terrex.structures.vec2 import Vec2
from terrex.structures.net_string import NetworkText
from terrex.structures.rgb import Rgb
from .base import (
    NetServerModule,
    NetClientModule,
    NetSyncModule,
)


class NetLiquidModule(NetServerModule):
    def __init__(self, liquids: List[Liquid]):
        self.liquids = liquids

    @classmethod
    def read(cls, reader: Reader) -> 'NetLiquidModule':
        count = reader.read_ushort()
        liquids = [Liquid.read(reader) for _ in range(count)]
        return cls(liquids)

    def write(self, writer: Writer) -> None:
        writer.write_ushort(len(self.liquids))
        for liquid in self.liquids:
            liquid.write(writer)


class NetTextModule(NetServerModule):
    def __init__(self, author_id: int, text: NetworkText, color: Rgb):
        self.author_id = author_id
        self.text = text
        self.color = color

    @classmethod
    def read(cls, reader: Reader) -> 'NetTextModule':
        author_id = reader.read_byte()
        text = NetworkText.read(reader)
        color = Rgb.read(reader)
        return cls(author_id, text, color)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.author_id)
        self.text.write(writer)
        self.color.write(writer)


class LoadNetModuleClientText(NetClientModule):
    def __init__(self, command: str, text: str):
        self.command = command
        self.text = text

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleClientText':
        # Fallback read, may not be accurate
        command = reader.read_string()
        text = reader.read_string()
        return cls(command, text)

    def write(self, writer: Writer) -> None:
        writer.write_string(self.command)
        writer.write_string(self.text)


class NetPingModule(NetSyncModule):
    def __init__(self, pos: Vec2):
        self.pos = pos

    @classmethod
    def read(cls, reader: Reader) -> 'NetPingModule':
        pos = Vec2.read(reader)
        return cls(pos)

    def write(self, writer: Writer) -> None:
        self.pos.write(writer)


class NetAmbienceModule(NetServerModule):
    def __init__(self, player_id: int, rand_next_num: int, sky_entity_type: 'SkyEntityType'):
        self.player_id = player_id
        self.rand_next_num = rand_next_num
        self.sky_entity_type = sky_entity_type

    @classmethod
    def read(cls, reader: Reader) -> 'NetAmbienceModule':
        player_id = reader.read_byte()
        rand_next_num = reader.read_int()
        sky_entity_type = SkyEntityType(reader.read_byte())
        return cls(player_id, rand_next_num, sky_entity_type)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_int(self.rand_next_num)
        writer.write_byte(self.sky_entity_type.value)


class NetBestiaryModule(NetServerModule):
    def __init__(self, bestiary: Bestiary):
        self.bestiary = bestiary

    @classmethod
    def read(cls, reader: Reader) -> 'NetBestiaryModule':
        bestiary = Bestiary.read(reader)
        return cls(bestiary)

    def write(self, writer: Writer) -> None:
        self.bestiary.write(writer)


class NetCreativePowersModule(NetSyncModule):
    def __init__(self, power: CreativePower):
        self.power = power

    @classmethod
    def read(cls, reader: Reader) -> 'NetCreativePowersModule':
        power = CreativePower.read(reader)
        return cls(power)

    def write(self, writer: Writer) -> None:
        self.power.write(writer)


class NetCreativeUnlocksPlayerReportModule(NetClientModule):
    def __init__(self, player_id: int, item_id: int, amount: int):
        self.player_id = player_id
        self.item_id = item_id
        self.amount = amount

    @classmethod
    def read(cls, reader: Reader) -> 'NetCreativeUnlocksPlayerReportModule':
        player_id = reader.read_byte()
        item_id = reader.read_ushort()
        amount = reader.read_ushort()
        return cls(player_id, item_id, amount)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_ushort(self.item_id)
        writer.write_ushort(self.amount)


from enum import IntEnum

class TeleportPylonOperation(IntEnum):
    AddForClient = 0
    RemoveForClient = 1
    HandleTeleportRequest = 2


class NetTeleportPylonModule(NetSyncModule):
    def __init__(self, operation: 'TeleportPylonOperation', x: int, y: int, pylon_type: 'TeleportPylonType'):
        self.operation = operation
        self.x = x
        self.y = y
        self.pylon_type = pylon_type

    @classmethod
    def read(cls, reader: Reader) -> 'NetTeleportPylonModule':
        operation = TeleportPylonOperation(reader.read_byte())
        x = reader.read_short()
        y = reader.read_short()
        pylon_type = TeleportPylonType(reader.read_byte())
        return cls(operation, x, y, pylon_type)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.operation.value)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_byte(self.pylon_type.value)

class NetParticlesModule(NetSyncModule):
    def __init__(self, particle_orchestra_type: int, particle_orchestra_settings: ParticleOrchestraSettings):
        self.particle_orchestra_type = particle_orchestra_type
        self.particle_orchestra_settings = particle_orchestra_settings

    @classmethod
    def read(cls, reader: Reader) -> 'NetParticlesModule':
        particle_orchestra_type = reader.read_byte()
        particle_orchestra_settings = ParticleOrchestraSettings.read(reader)
        return cls(particle_orchestra_type,particle_orchestra_settings)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.particle_orchestra_type)
        self.particle_orchestra_settings.write(writer)


class NetCreativePowerPermissionsModule(NetServerModule):
    def __init__(self, zero: int, power_id: int, level: int):
        self.zero = zero
        self.power_id = power_id
        self.level = level

    @classmethod
    def read(cls, reader: Reader) -> 'NetCreativePowerPermissionsModule':
        zero = reader.read_byte()
        if (zero == 0):
            power_id = reader.read_ushort()
            level = reader.read_byte()
        return cls(zero, power_id, level)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.zero)
        writer.write_ushort(self.power_id)
        writer.write_byte(self.level)

class NetBannersMessageType(IntEnum):
    FullState = 0
    KillCountUpdate = 1
    ClaimCountUpdate = 2
    ClaimRequest = 3
    ClaimResponse = 4


class NetBannersModule(NetServerModule):
    def __init__(
        self,
        msg_type: NetBannersMessageType,
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
        msg_type = NetBannersMessageType(reader.read_byte())
        banner_data = None
        banner_id = None
        kill_count = None
        claimable_count = None
        amount = None
        granted = None

        kill_counts = None
        claimable_banners = None
        if msg_type == NetBannersMessageType.FullState:
            num = reader.read_short()
            kill_counts = [reader.read_int() for _ in range(num)]
            claimable_banners = None
            if reader.version >= 289:
                num_claim = reader.read_short()
                claimable_banners = [reader.read_ushort() for _ in range(num_claim)]
        elif msg_type == NetBannersMessageType.KillCountUpdate:
            banner_id = reader.read_short()
            kill_count = reader.read_int()
        elif msg_type == NetBannersMessageType.ClaimCountUpdate:
            banner_id = reader.read_short()
            claimable_count = reader.read_ushort()
        elif msg_type == NetBannersMessageType.ClaimRequest:
            banner_id = reader.read_short()
            amount = reader.read_ushort()
        elif msg_type == NetBannersMessageType.ClaimResponse:
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
        if self.msg_type == NetBannersMessageType.FullState:
            if self.kill_counts is not None:
                writer.write_short(len(self.kill_counts))
                for kc in self.kill_counts:
                    writer.write_int(kc)
            if self.claimable_banners is not None:
                writer.write_short(len(self.claimable_banners))
                for cb in self.claimable_banners:
                    writer.write_ushort(cb)
        elif self.msg_type == NetBannersMessageType.KillCountUpdate:
            writer.write_short(self.banner_id)
            writer.write_int(self.kill_count)
        elif self.msg_type == NetBannersMessageType.ClaimCountUpdate:
            writer.write_short(self.banner_id)
            writer.write_ushort(self.claimable_count)
        elif self.msg_type == NetBannersMessageType.ClaimRequest:
            writer.write_short(self.banner_id)
            writer.write_ushort(self.amount)
        elif self.msg_type == NetBannersMessageType.ClaimResponse:
            writer.write_short(self.banner_id)
            writer.write_ushort(self.amount)
            writer.write_bool(self.granted)


class NetCraftingRequestModule(NetServerModule):
    def __init__(self, items: list[tuple[int, int]], chests: list[int | None]):
        self.items = items  # (item_id, stack)
        self.chests = chests  # chest.index or None (-1)

    @classmethod
    def read(cls, reader: Reader) -> 'NetCraftingRequestModule':
        num_items = reader.read_7bit_encoded_int()
        items = []
        for _ in range(num_items):
            item_id = reader.read_int()
            stack = reader.read_7bit_encoded_int()
            items.append((item_id, stack))
        num_chests = reader.read_7bit_encoded_int()
        chests = []
        for _ in range(num_chests):
            idx = reader.read_7bit_encoded_int()
            chests.append(None if idx < 0 else idx)
        return cls(items, chests)

    
    def write(self, writer: Writer) -> None:
        writer.write_7bit_encoded_int(len(self.items))
        for item_id, stack in self.items:
            writer.write_int(item_id)
            writer.write_7bit_encoded_int(stack)
        writer.write_7bit_encoded_int(len(self.chests))
        for chest in self.chests:
            idx = -1 if chest is None else chest
            writer.write_7bit_encoded_int(idx)


class NetCraftingResponseModule(NetClientModule):
    def __init__(self, approved: bool):
        self.approved = approved

    def read(cls, reader: Reader) -> 'NetCraftingResponseModule':
        approved = reader.read_bool()
        return cls(approved)

    @classmethod
    def write(self, writer: Writer) -> None:
        writer.write_bool(self.approved)


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


class NetUnbreakableWallScanModule(NetServerModule):
    def __init__(self, player_id: int, inside_unbreakable_walls: bool):
        self.player_id = player_id
        self.inside_unbreakable_walls = inside_unbreakable_walls

    @classmethod
    def read(cls, reader: Reader) -> 'NetUnbreakableWallScanModule':
        player_id = reader.read_byte()
        inside = reader.read_bool()
        return cls(player_id, inside)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_bool(self.inside_unbreakable_walls)


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
