from terrex.packets.base import ClientPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class ToggleBirthdayParty(ClientPacket):
    id = 111

    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        pass

    def handle(self, world, player, evman):
        pass

ToggleBirthdayParty.register()