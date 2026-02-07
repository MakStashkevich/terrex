from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader


class SetEvent(ServerPacket):
    id = PacketIds.NOTIFY_PLAYER_EVENT.value

    def __init__(self, event_id: int = 0):
        self.event_id = event_id

    def read(self, reader: Reader):
        self.event_id = reader.read_short()


SetEvent.register()
