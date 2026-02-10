from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader


class CrystalInvasionWait(ServerPacket):
    id = PacketIds.CRYSTAL_INVASION_SEND_WAIT_TIME

    def __init__(self, time_until_next_wave: int = 0):
        self.time_until_next_wave = time_until_next_wave

    def read(self, reader: Reader):
        self.time_until_next_wave = reader.read_int()


CrystalInvasionWait.register()
