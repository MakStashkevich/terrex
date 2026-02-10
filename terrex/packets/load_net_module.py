from terrex.events.events import Event
from terrex.structures.game_content.net_modules.net_module import NetModule
from terrex.packets.base import SyncPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

from terrex.structures.game_content.net_modules import (
    NetTextModule,
    net_module_registry,
)


class LoadNetModule(SyncPacket):
    id = PacketIds.LOAD_NET_MODULE

    module: NetModule

    def __init__(self, module: NetModule = None):
        self.module = module

    def read(self, reader: Reader) -> None:
        module_id = reader.read_ushort()
        module_cls = net_module_registry.get(module_id)
        if module_cls is None:
            raise ValueError(f"Unknown NetModule variant: {module_id}")
        if not issubclass(module_cls, NetModule):
            raise ValueError(
                f"Registry entry for {module_id} is not a subclass of NetModule"
            )
        module = module_cls()
        module.read(reader)
        self.module = module

    def write(self, writer: Writer) -> None:
        writer.write_ushort(self.module.id)
        self.module.write(writer)

    def handle(self, world, player, evman):
        if isinstance(self.module, NetTextModule):
            evman.raise_event(Event.Chat, self.module)


LoadNetModule.register()
