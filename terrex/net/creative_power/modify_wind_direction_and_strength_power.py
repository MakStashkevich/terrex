from dataclasses import dataclass

from terrex.net.creative_power.creative_power import CreativePower
from terrex.net.streamer import Reader, Writer


@dataclass()
class ModifyWindDirectionAndStrengthPower(CreativePower):
    id: int = 6

    @classmethod
    def create(cls) -> "ModifyWindDirectionAndStrengthPower":
        return cls()

    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        pass
