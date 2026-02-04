from typing import Optional
from dataclasses import dataclass, field
from terrex.util.streamer import Reader, Writer

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
class WeaponRack(TileEntityBase):
    type: int = 4
    item_type: int = 0
    item_prefix: int = 0
    item_stack: int = 0

@dataclass
class FoodPlatter(TileEntityBase):
    type: int = 6
    item_type: int = 0
    item_prefix: int = 0
    item_stack: int = 0

@dataclass
class Pylon(TileEntityBase):
    type: int = 7

# Placeholder for incomplete
@dataclass
class DisplayDoll(TileEntityBase):
    type: int = 3
    flags: list[int] = field(default_factory=list)

@dataclass
class HatRack(TileEntityBase):
    type: int = 5
    flags: int = 0

TileEntity = (
    TrainingDummy | ItemFrame | LogicSensor | DisplayDoll | WeaponRack | HatRack | FoodPlatter | Pylon
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
        return ItemFrame(type=typ, id=id_, x=x, y=y, item_type=item_type, item_prefix=item_prefix, item_stack=item_stack)
    elif typ == 2:
        logic_check_type = reader.read_byte()
        on = reader.read_bool()
        return LogicSensor(type=typ, id=id_, x=x, y=y, logic_check_type=logic_check_type, on=on)
    elif typ == 3:
        # TODO full impl
        return DisplayDoll(type=typ, id=id_, x=x, y=y)
    elif typ == 4:
        item_type = reader.read_ushort()
        item_prefix = reader.read_byte()
        item_stack = reader.read_ushort()
        return WeaponRack(type=typ, id=id_, x=x, y=y, item_type=item_type, item_prefix=item_prefix, item_stack=item_stack)
    elif typ == 5:
        # TODO full impl
        flags = reader.read_byte()
        return HatRack(type=typ, id=id_, x=x, y=y, flags=flags)
    elif typ == 6:
        item_type = reader.read_ushort()
        item_prefix = reader.read_byte()
        item_stack = reader.read_ushort()
        return FoodPlatter(type=typ, id=id_, x=x, y=y, item_type=item_type, item_prefix=item_prefix, item_stack=item_stack)
    elif typ == 7:
        return Pylon(type=typ, id=id_, x=x, y=y)
    else:
        raise ValueError(f"Unknown TileEntity type: {typ}")

def write_tile_entity(entity: TileEntity, writer: Writer) -> None:
    # TODO: implement based on type
    pass
