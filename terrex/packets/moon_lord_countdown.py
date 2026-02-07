from terrex.packets.base import ServerPacket
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader


class MoonLordCountdown(ServerPacket):
    id = PacketIds.MOON_LORD_COUNTDOWN.value

    def __init__(self, countdown: int = 0):
        self.countdown = countdown

    def read(self, reader: Reader):
        self.countdown = reader.read_int()


MoonLordCountdown.register()
