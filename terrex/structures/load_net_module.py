from typing import List
from terrex.util.streamer import Reader, Writer
from terrex.structures.liquid import Liquid
from terrex.structures.bestiary import Bestiary
from terrex.structures.creative_power import CreativePower
from terrex.structures.vec2 import Vec2
from terrex.structures.net_string import NetString
from terrex.structures.rgb import Rgb
from .load_net_packet import (
    LoadNetServerPacket,
    LoadNetClientPacket,
    LoadNetSyncPacket,
)


class LoadNetModuleLiquid(LoadNetServerPacket):
    def __init__(self, liquids: List[Liquid]):
        self.liquids = liquids

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleLiquid':
        count = reader.read_ushort()
        liquids = [Liquid.read(reader) for _ in range(count)]
        return cls(liquids)

    def write(self, writer: Writer) -> None:
        writer.write_ushort(len(self.liquids))
        for liquid in self.liquids:
            liquid.write(writer)


class LoadNetModuleServerText(LoadNetServerPacket):
    def __init__(self, author: int, text: NetString, color: Rgb):
        self.author = author
        self.text = text
        self.color = color

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleServerText':
        author = reader.read_byte()
        text = NetString.read(reader)
        color = Rgb.read(reader)
        return cls(author, text, color)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.author)
        self.text.write(writer)
        self.color.write(writer)


class LoadNetModuleClientText(LoadNetClientPacket):
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


class LoadNetModulePing(LoadNetSyncPacket):
    def __init__(self, pos: Vec2):
        self.pos = pos

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModulePing':
        pos = Vec2.read(reader)
        return cls(pos)

    def write(self, writer: Writer) -> None:
        self.pos.write(writer)


class LoadNetModuleAmbience(LoadNetServerPacket):
    def __init__(self, player: int, num: int, ty: int):
        self.player = player
        self.num = num
        self.ty = ty

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleAmbience':
        player = reader.read_byte()
        num = reader.read_int()
        ty = reader.read_byte()
        return cls(player, num, ty)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player)
        writer.write_int(self.num)
        writer.write_byte(self.ty)


class LoadNetModuleBestiary(LoadNetServerPacket):
    def __init__(self, bestiary: Bestiary):
        self.bestiary = bestiary

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleBestiary':
        bestiary = Bestiary.read(reader)
        return cls(bestiary)

    def write(self, writer: Writer) -> None:
        self.bestiary.write(writer)


class LoadNetModuleCreativeUnlocks(LoadNetServerPacket):
    def __init__(self, item_id: int, sacrifice_count: int):
        self.item_id = item_id
        self.sacrifice_count = sacrifice_count

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleCreativeUnlocks':
        item_id = reader.read_short()
        sacrifice_count = reader.read_ushort()
        return cls(item_id, sacrifice_count)

    def write(self, writer: Writer) -> None:
        writer.write_short(self.item_id)
        writer.write_ushort(self.sacrifice_count)


class LoadNetModuleCreativePowers(LoadNetSyncPacket):
    def __init__(self, power: CreativePower):
        self.power = power

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleCreativePowers':
        power = CreativePower.read(reader)
        return cls(power)

    def write(self, writer: Writer) -> None:
        self.power.write(writer)


class LoadNetModuleCreativeUnlocksPlayerReport(LoadNetClientPacket):
    def __init__(self, zero: int, item_id: int, amount: int):
        self.zero = zero
        self.item_id = item_id
        self.amount = amount

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleCreativeUnlocksPlayerReport':
        zero = reader.read_byte()
        item_id = reader.read_ushort()
        amount = reader.read_ushort()
        return cls(zero, item_id, amount)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.zero)
        writer.write_ushort(self.item_id)
        writer.write_ushort(self.amount)


class LoadNetModuleTeleportPylon(LoadNetSyncPacket):
    def __init__(self, ty: int, x: int, y: int, pylon_type: int):
        self.ty = ty
        self.x = x
        self.y = y
        self.pylon_type = pylon_type

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleTeleportPylon':
        ty = reader.read_byte()
        x = reader.read_short()
        y = reader.read_short()
        pylon_type = reader.read_byte()
        return cls(ty, x, y, pylon_type)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.ty)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_byte(self.pylon_type)


class LoadNetModuleParticles(LoadNetSyncPacket):
    def __init__(self, ty: int, pos: Vec2, vel: Vec2, packed_shader_index: int, player: int):
        self.ty = ty
        self.pos = pos
        self.vel = vel
        self.packed_shader_index = packed_shader_index
        self.player = player

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleParticles':
        ty = reader.read_byte()
        pos = Vec2.read(reader)
        vel = Vec2.read(reader)
        packed_shader_index = reader.read_int()
        player = reader.read_byte()
        return cls(ty, pos, vel, packed_shader_index, player)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.ty)
        self.pos.write(writer)
        self.vel.write(writer)
        writer.write_int(self.packed_shader_index)
        writer.write_byte(self.player)


class LoadNetModuleCreativePowerPermissions(LoadNetServerPacket):
    def __init__(self, zero: int, power_id: int, level: int):
        self.zero = zero
        self.power_id = power_id
        self.level = level

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleCreativePowerPermissions':
        zero = reader.read_byte()
        power_id = reader.read_ushort()
        level = reader.read_byte()
        return cls(zero, power_id, level)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.zero)
        writer.write_ushort(self.power_id)
        writer.write_byte(self.level)