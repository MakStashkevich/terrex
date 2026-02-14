from dataclasses import dataclass

from terrex.structures.game_content.creative.creative_power.creative_power import CreativePower
from terrex.util.streamer import Reader, Writer


@dataclass()
class StartNightImmediatelyPower(CreativePower):
    id: int = 3

    @classmethod
    def create(cls) -> "StartNightImmediatelyPower":
        return cls()

    def read(self, reader: Reader) -> None:
        pass

    def write(self, writer: Writer) -> None:
        pass
