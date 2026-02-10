from typing import Dict, Type
from terrex.events.events import Event
from terrex.structures.game_content.net_modules.base import NetModule
from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

from terrex.structures.game_content.net_modules.net_modules import (
    NetLiquidModule,
    NetTextModule,
    NetPingModule,
    NetAmbienceModule,
    NetBestiaryModule,
    NetCreativePowersModule,
    NetCreativeUnlocksPlayerReportModule,
    NetTeleportPylonModule,
    NetParticlesModule,
    NetCreativePowerPermissionsModule,
    NetBannersModule,
    NetCraftingRequestModule,
    NetTagEffectModule,
    NetLeashedEntityModule,
    NetUnbreakableWallScanModule,
)

# NetworkInitializer.Load()
NET_MODULES: Dict[int, Type["NetModule"]] = {
    0: NetLiquidModule,
    1: NetTextModule,
    2: NetPingModule,
    3: NetAmbienceModule,
    4: NetBestiaryModule,
    5: NetCreativePowersModule,
    6: NetCreativeUnlocksPlayerReportModule,
    7: NetTeleportPylonModule,
    8: NetParticlesModule,
    9: NetCreativePowerPermissionsModule,
    10: NetBannersModule,
    11: NetCraftingRequestModule,
    12: NetTagEffectModule,
    13: NetLeashedEntityModule,
    14: NetUnbreakableWallScanModule,
}


class LoadNetModule(SyncPacket):
    id = PacketIds.LOAD_NET_MODULE.value

    def __init__(self, variant: int = 0, net_module: NetModule = None):
        self.variant = variant
        self.net_module = net_module

    def read(self, reader: Reader) -> None:
        self.variant = reader.read_ushort()
        net_module = NET_MODULES.get(self.variant)
        if net_module is None:
            raise ValueError(f"Unknown variant LoadNetModule: {self.variant}")
        self.net_module = net_module.read(reader)

    def write(self, writer: Writer) -> None:
        writer.write_ushort(self.variant)
        self.net_module.write(writer)

    def handle(self, world, player, evman):
        if self.variant == 1 and isinstance(
            self.net_module, NetTextModule
        ):  # server text
            evman.raise_event(Event.Chat, self.net_module)


LoadNetModule.register()
