from terrex.structures.game_content.creative.creative_power import CREATIVE_POWER_REGISTRY
from terrex.structures.game_content.creative.creative_power.creative_power import CreativePower
from terrex.util.streamer import Reader, Writer
from .base import NetSyncModule


class NetCreativePowersModule(NetSyncModule):
    power_id: int
    power: CreativePower

    def __init__(self, power: CreativePower):
        self.power = power

    @classmethod
    def read(cls, reader: Reader) -> "CreativePower":
        power_id = reader.read_byte()
        power_cls = CREATIVE_POWER_REGISTRY.get(power_id)
        if power_cls is None:
            raise ValueError(f"Unknown CreativePower variant: {power_id}")
        if not issubclass(power_cls, CreativePower):
            raise ValueError(
                f"Registry entry for {power_id} is not a subclass of CreativePowerBase"
            )
        power = power_cls()
        power.read(reader)
        return cls(power_id=power_id, power=power)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.power_id)
        self.power.write(writer)
