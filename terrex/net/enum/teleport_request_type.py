from enum import IntEnum


class TeleportRequestType(IntEnum):
    TeleportationPotion = 0  # to random pos
    MagicConch = 1
    Shellphone_Ocean = 1
    DemonConch = 2
    Shellphone_Underworld = 2
    Shellphone_Spawn = 3
    PlayerNoSpaceTeleport = 4  # after dismount
