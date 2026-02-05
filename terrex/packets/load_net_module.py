from typing import Dict, Type
from terrex.structures.load_net_packet import LoadNetPacket
from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

from terrex.structures.load_net_module import (
    LoadNetModuleLiquid,
    LoadNetModuleServerText,
    LoadNetModulePing,
    LoadNetModuleAmbience,
    LoadNetModuleBestiary,
    LoadNetModuleCreativeUnlocks,
    LoadNetModuleCreativePowers,
    LoadNetModuleCreativeUnlocksPlayerReport,
    LoadNetModuleTeleportPylon,
    LoadNetModuleParticles,
    LoadNetModuleCreativePowerPermissions,
)

BODY_CLASSES: Dict[int, Type['LoadNetPacket']] = {
    0: LoadNetModuleLiquid,
    1: LoadNetModuleServerText,
    2: LoadNetModulePing,
    3: LoadNetModuleAmbience,
    4: LoadNetModuleBestiary,
    5: LoadNetModuleCreativeUnlocks,
    6: LoadNetModuleCreativePowers,
    7: LoadNetModuleCreativeUnlocksPlayerReport,
    8: LoadNetModuleTeleportPylon,
    9: LoadNetModuleParticles,
    10: LoadNetModuleCreativePowerPermissions,
}

class LoadNetModule(SyncPacket):
    id = PacketIds.LOAD_NET_MODULE.value

    def __init__(self):
        self.variant: int = 0
        self.body: LoadNetPacket = None

    def read(self, reader: Reader) -> None:
        self.variant = reader.read_ushort()
        body_cls = BODY_CLASSES.get(self.variant)
        if body_cls is None:
            raise ValueError(f"Неизвестный вариант LoadNetModule: {self.variant}")
        self.body = body_cls.read(reader)

    def write(self, writer: Writer) -> None:
        writer.write_ushort(self.variant)
        self.body.write(writer)

LoadNetModule.register()