from dataclasses import dataclass

from terrex.net.creative_power.creative_power import CreativePower
from terrex.net.streamer import Reader, Writer


@dataclass()
class FreezeRainPower(CreativePower):
    id: int = 9
    enabled: bool | None = None

    @classmethod
    def create(cls, enabled: bool = False) -> "FreezeRainPower":
        obj = cls()
        obj.enabled = enabled
        return obj

    def read(self, reader: Reader) -> None:
        self.enabled = reader.read_bool()

    def write(self, writer: Writer) -> None:
        writer.write_bool(self.enabled)
