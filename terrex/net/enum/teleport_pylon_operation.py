from enum import IntEnum


class TeleportPylonOperation(IntEnum):
    AddForClient = 0
    RemoveForClient = 1
    HandleTeleportRequest = 2
