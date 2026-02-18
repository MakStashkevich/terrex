from dataclasses import dataclass

from terrex.net.creative_power.creative_power import CreativePower
from terrex.net.streamer import Reader, Writer


@dataclass()
class StartDayImmediatelyPower(CreativePower):
    id: int = 1

    @classmethod
    def create(cls) -> "StartDayImmediatelyPower":
        return cls()

    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        pass
