from dataclasses import dataclass

from terrex.net.creative_power import (
    CreativePower,
    creative_power_registry,
)
from terrex.net.streamer import Reader, Writer

from .net_module import NetSyncModule


@dataclass()
class NetCreativePowersModule(NetSyncModule):
    id: int = 5
    power: CreativePower | None = None

    @classmethod
    def create(cls, power: CreativePower) -> "NetCreativePowersModule":
        obj = cls()
        obj.power = power
        return obj

    def read(self, reader: Reader) -> None:
        power_id = reader.read_byte()
        power_cls = creative_power_registry.get(power_id)
        if power_cls is None:
            raise ValueError(f"Unknown CreativePower variant: {power_id}")
        if not issubclass(power_cls, CreativePower):
            raise ValueError(f"Registry entry for {power_id} is not a subclass of CreativePower")
        self.power = power_cls()
        self.power.read(reader)

    def write(self, writer: Writer) -> None:
        if self.power is None:
            raise ValueError("power must not be None")
        writer.write_byte(self.power.id)
        self.power.write(writer)
