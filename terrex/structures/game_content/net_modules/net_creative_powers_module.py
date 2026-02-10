from terrex.structures.game_content.creative.creative_power import CreativePower
from terrex.util.streamer import Reader, Writer
from .base import NetSyncModule


class NetCreativePowersModule(NetSyncModule):
    def __init__(self, power: CreativePower):
        self.power = power

    @classmethod
    def read(cls, reader: Reader) -> 'NetCreativePowersModule':
        power = CreativePower.read(reader)
        return cls(power)

    def write(self, writer: Writer) -> None:
        self.power.write(writer)
