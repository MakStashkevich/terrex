from typing import Optional
from dataclasses import dataclass, field
from terrex.util.streamer import Reader, Writer
from terrex.data.item import Item


@dataclass
class TileEntityBase:
    id: int = 0
    x: int = 0
    y: int = 0


@dataclass
class TrainingDummy(TileEntityBase):
    type: int = 0
    npc_index: int = 0


@dataclass
class ItemFrame(TileEntityBase):
    type: int = 1
    item_type: int = 0
    item_prefix: int = 0
    item_stack: int = 0


@dataclass
class LogicSensor(TileEntityBase):
    type: int = 2
    logic_check_type: int = 0
    on: bool = False


@dataclass
class DisplayDoll(TileEntityBase):
    type: int = 3
    pose: int = 0
    equip: list[Optional[Item]] = field(default_factory=lambda: [None] * 9)
    dyes: list[Optional[Item]] = field(default_factory=lambda: [None] * 9)
    misc: list[Optional[Item]] = field(default_factory=lambda: [None] * 8)


@dataclass
class WeaponRack(TileEntityBase):
    type: int = 4
    item_type: int = 0
    item_prefix: int = 0
    item_stack: int = 0


@dataclass
class HatRack(TileEntityBase):
    type: int = 5
    items: list[Optional[Item]] = field(default_factory=lambda: [None, None])
    dyes: list[Optional[Item]] = field(default_factory=lambda: [None, None])


@dataclass
class FoodPlatter(TileEntityBase):
    type: int = 6
    item_type: int = 0
    item_prefix: int = 0
    item_stack: int = 0


@dataclass
class TeleportationPylon(TileEntityBase):
    type: int = 7


@dataclass
class DeadCellsDisplayJar(TileEntityBase):
    type: int = 8
    item_type: int = 0
    item_prefix: int = 0
    item_stack: int = 0


@dataclass
class LeashedEntityAnchorWithItem(TileEntityBase):
    item_type: int = 0


@dataclass
class KiteAnchor(LeashedEntityAnchorWithItem):
    type: int = 9
    item_type: int = 0


@dataclass
class CritterAnchor(LeashedEntityAnchorWithItem):
    type: int = 10
    item_type: int = 0


TileEntity = (
    TrainingDummy
    | ItemFrame
    | LogicSensor
    | DisplayDoll
    | WeaponRack
    | HatRack
    | FoodPlatter
    | TeleportationPylon
    | DeadCellsDisplayJar
    | KiteAnchor
    | CritterAnchor
)


def read_tile_entity(reader: Reader) -> TileEntity:
    typ = reader.read_byte()
    id_ = reader.read_int()
    x = reader.read_short()
    y = reader.read_short()
    if typ == 0:
        npc_index = reader.read_ushort()
        return TrainingDummy(type=typ, id=id_, x=x, y=y, npc_index=npc_index)
    elif typ == 1:
        item_type = reader.read_ushort()
        item_prefix = reader.read_byte()
        item_stack = reader.read_ushort()
        return ItemFrame(
            type=typ,
            id=id_,
            x=x,
            y=y,
            item_type=item_type,
            item_prefix=item_prefix,
            item_stack=item_stack,
        )
    elif typ == 2:
        logic_check_type = reader.read_byte()
        on = reader.read_bool()
        return LogicSensor(
            type=typ, id=id_, x=x, y=y, logic_check_type=logic_check_type, on=on
        )
    elif typ == 3:
        game_version = 317
        bits_byte = reader.read_byte()
        bits_byte1 = reader.read_byte()
        pose = 0
        if game_version >= 307:
            pose = reader.read_byte()
        bits_byte2 = 0
        if game_version >= 308:
            bits_byte2 = reader.read_byte()
        has_item = False
        if game_version == 311:
            has_item = bool(bits_byte2 & 2)
            bits_byte2 &= ~2
        num_equip = bits_byte | (256 if (bits_byte2 & 2) else 0)
        equip = [None] * 9
        for i in range(9):
            if num_equip & (1 << i):
                item_id = reader.read_ushort()
                prefix = reader.read_byte()
                stack = reader.read_ushort()
                equip[i] = Item(item_id=item_id, prefix=prefix, stacks=stack, net_id=0, position=None, velocity=None)
        num_dyes = bits_byte1 | (256 if (bits_byte2 & 4) else 0)
        dyes = [None] * 9
        for j in range(9):
            if num_dyes & (1 << j):
                item_id = reader.read_ushort()
                prefix = reader.read_byte()
                stack = reader.read_ushort()
                dyes[j] = Item(item_id=item_id, prefix=prefix, stacks=stack, net_id=0, position=None, velocity=None)
        misc = [None] * 8
        for k in range(8):
            if bits_byte2 & (1 << k):
                item_id = reader.read_ushort()
                prefix = reader.read_byte()
                stack = reader.read_ushort()
                misc[k] = Item(item_id=item_id, prefix=prefix, stacks=stack, net_id=0, position=None, velocity=None)
        if has_item:
            item_id = reader.read_ushort()
            prefix = reader.read_byte()
            stack = reader.read_ushort()
            equip[8] = Item(item_id=item_id, prefix=prefix, stacks=stack, net_id=0, position=None, velocity=None)
        return DisplayDoll(type=typ, id=id_, x=x, y=y, pose=pose, equip=equip, dyes=dyes, misc=misc)
    elif typ == 4:
        item_type = reader.read_ushort()
        item_prefix = reader.read_byte()
        item_stack = reader.read_ushort()
        return WeaponRack(
            type=typ,
            id=id_,
            x=x,
            y=y,
            item_type=item_type,
            item_prefix=item_prefix,
            item_stack=item_stack,
        )
    elif typ == 5:
        flags = reader.read_byte()
        items = [None, None]
        dyes = [None, None]
        for i in range(2):
            if flags & (1 << i):
                item_id = reader.read_ushort()
                prefix = reader.read_byte()
                stack = reader.read_ushort()
                items[i] = Item(item_id=item_id, prefix=prefix, stacks=stack, net_id=0, position=None, velocity=None)
        for j in range(2):
            if flags & (1 << (j + 2)):
                item_id = reader.read_ushort()
                prefix = reader.read_byte()
                stack = reader.read_ushort()
                dyes[j] = Item(item_id=item_id, prefix=prefix, stacks=stack, net_id=0, position=None, velocity=None)
        return HatRack(type=typ, id=id_, x=x, y=y, items=items, dyes=dyes)
    elif typ == 6:
        item_type = reader.read_ushort()
        item_prefix = reader.read_byte()
        item_stack = reader.read_ushort()
        return FoodPlatter(
            type=typ,
            id=id_,
            x=x,
            y=y,
            item_type=item_type,
            item_prefix=item_prefix,
            item_stack=item_stack,
        )
    elif typ == 7:
        return TeleportationPylon(type=typ, id=id_, x=x, y=y)
    # added on v1.4.5.0+
    elif typ == 8:
        item_type = reader.read_ushort()
        item_prefix = reader.read_byte()
        item_stack = reader.read_ushort()
        return DeadCellsDisplayJar(
            type=typ,
            id=id_,
            x=x,
            y=y,
            item_type=item_type,
            item_prefix=item_prefix,
            item_stack=item_stack,
        )
    elif typ == 9:
        item_type = reader.read_ushort()
        return KiteAnchor(type=typ, id=id_, x=x, y=y, item_type=item_type)
    elif typ == 10:
        item_type = reader.read_ushort()
        return CritterAnchor(type=typ, id=id_, x=x, y=y, item_type=item_type)
    else:
        raise ValueError(f"Unknown TileEntity type: {typ}")


def write_tile_entity(entity: TileEntity, writer: Writer) -> None:
    # TODO: implement based on type
    pass
