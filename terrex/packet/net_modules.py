from terrex.event.types import ChatEvent
from terrex.packet.base import SyncPacket
from terrex.net.module import (
    NetTextModule,
    net_module_registry,
)
from terrex.net.module.net_module import NetModule
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class NetModules(SyncPacket):
    id = MessageID.NetModules

    module: NetModule

    def __init__(self, module: NetModule = None):
        self.module = module

    def read(self, reader: Reader) -> None:
        module_id = reader.read_ushort()
        module_cls = net_module_registry.get(module_id)
        if module_cls is None:
            raise ValueError(f"Unknown NetModule variant: {module_id}")
        if not issubclass(module_cls, NetModule):
            raise ValueError(f"Registry entry for {module_id} is not a subclass of NetModule")
        module = module_cls()
        module.read(reader)
        self.module = module

    def write(self, writer: Writer) -> None:
        writer.write_ushort(self.module.id)
        self.module.write(writer)

    async def handle(self, world, player, evman):
        if (
            isinstance(self.module, NetTextModule)
            and self.module.author_id is not None
            and self.module.text is not None
            # ignore client chat commands
            and self.module.chat_command_id is None
        ):
            await evman.raise_event(ChatEvent(self, self.module.author_id, self.module.text.text, self.module.chat_command_id))
