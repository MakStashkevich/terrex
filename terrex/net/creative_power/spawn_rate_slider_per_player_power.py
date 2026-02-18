from dataclasses import dataclass

from terrex.net.creative_power.creative_power import CreativePower
from terrex.net.streamer import Reader, Writer


@dataclass()
class SpawnRateSliderPerPlayerPower(CreativePower):
    id: int = 14
    value: float | None = None

    @classmethod
    def create(cls, value: float = 0.0) -> "SpawnRateSliderPerPlayerPower":
        obj = cls()
        obj.value = value
        return obj

    def read(self, reader: Reader) -> None:
        self.value = reader.read_single()

    def write(self, writer: Writer) -> None:
        writer.write_single(self.value)
