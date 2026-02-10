from dataclasses import dataclass

from terrex.structures.game_content.creative.creative_power.creative_power import CreativePower
from terrex.util.streamer import Reader, Writer


@dataclass
class FarPlacementRangePower(CreativePower):
    id: int = 11
    enabled: bool

    def read(self, reader: Reader) -> None:
        self.enabled = reader.read_bool()

    def write(self, writer: Writer) -> None:
        writer.write_bool(self.enabled)
