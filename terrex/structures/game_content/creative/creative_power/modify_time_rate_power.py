from dataclasses import dataclass

from terrex.structures.game_content.creative.creative_power.creative_power import CreativePower
from terrex.util.streamer import Reader, Writer


@dataclass
class ModifyTimeRatePower(CreativePower):
    id: int = 8
    value: float

    def read(self, reader: Reader) -> None:
        self.value = reader.read_single()

    def write(self, writer: Writer) -> None:
        writer.write_single(self.value)
