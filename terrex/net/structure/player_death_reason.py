from __future__ import annotations

from terrex.net.streamer import Reader, Writer


class PlayerDeathReason:
    HAS_KILLER = 0x01
    HAS_KILLING_NPC = 0x02
    HAS_PROJECTILE_IDX = 0x04
    HAS_TYPE_OF_DEATH = 0x08
    HAS_PROJECTILE_TYPE = 0x10
    HAS_ITEM_TYPE = 0x20
    HAS_ITEM_PREFIX = 0x40
    HAS_CUSTOM_REASON = 0x80

    def __init__(
        self,
        reason_flags: int = 0,
        killer_player_id: int | None = None,
        killing_npc_index: int | None = None,
        projectile_index: int | None = None,
        death_type: int | None = None,
        projectile_type: int | None = None,
        item_type: int | None = None,
        item_prefix: int | None = None,
        custom_reason: str | None = None,
    ):
        self.reason_flags = reason_flags
        self.killer_player_id = killer_player_id
        self.killing_npc_index = killing_npc_index
        self.projectile_index = projectile_index
        self.death_type = death_type
        self.projectile_type = projectile_type
        self.item_type = item_type
        self.item_prefix = item_prefix
        self.custom_reason = custom_reason

    @classmethod
    def read(cls, reader: Reader) -> PlayerDeathReason:
        reason_flags = reader.read_byte()
        killer_player_id = None
        if reason_flags & cls.HAS_KILLER:
            killer_player_id = reader.read_short()
        killing_npc_index = None
        if reason_flags & cls.HAS_KILLING_NPC:
            killing_npc_index = reader.read_short()
        projectile_index = None
        if reason_flags & cls.HAS_PROJECTILE_IDX:
            projectile_index = reader.read_short()
        death_type = None
        if reason_flags & cls.HAS_TYPE_OF_DEATH:
            death_type = reader.read_byte()
        projectile_type = None
        if reason_flags & cls.HAS_PROJECTILE_TYPE:
            projectile_type = reader.read_short()
        item_type = None
        if reason_flags & cls.HAS_ITEM_TYPE:
            item_type = reader.read_short()
        item_prefix = None
        if reason_flags & cls.HAS_ITEM_PREFIX:
            item_prefix = reader.read_byte()
        custom_reason = None
        if reason_flags & cls.HAS_CUSTOM_REASON:
            custom_reason = reader.read_dotnet_string()

        return cls(
            reason_flags,
            killer_player_id,
            killing_npc_index,
            projectile_index,
            death_type,
            projectile_type,
            item_type,
            item_prefix,
            custom_reason,
        )

    def write(self, writer: Writer) -> None:
        flags = 0
        if self.killer_player_id is not None:
            flags |= self.HAS_KILLER
        if self.killing_npc_index is not None:
            flags |= self.HAS_KILLING_NPC
        if self.projectile_index is not None:
            flags |= self.HAS_PROJECTILE_IDX
        if self.death_type is not None:
            flags |= self.HAS_TYPE_OF_DEATH
        if self.projectile_type is not None:
            flags |= self.HAS_PROJECTILE_TYPE
        if self.item_type is not None:
            flags |= self.HAS_ITEM_TYPE
        if self.item_prefix is not None:
            flags |= self.HAS_ITEM_PREFIX
        if self.custom_reason is not None:
            flags |= self.HAS_CUSTOM_REASON

        writer.write_byte(flags)

        if self.killer_player_id is not None:
            writer.write_short(self.killer_player_id)
        if self.killing_npc_index is not None:
            writer.write_short(self.killing_npc_index)
        if self.projectile_index is not None:
            writer.write_short(self.projectile_index)
        if self.death_type is not None:
            writer.write_byte(self.death_type)
        if self.projectile_type is not None:
            writer.write_short(self.projectile_type)
        if self.item_type is not None:
            writer.write_short(self.item_type)
        if self.item_prefix is not None:
            writer.write_byte(self.item_prefix)
        if self.custom_reason is not None:
            writer.write_dotnet_string(self.custom_reason)
