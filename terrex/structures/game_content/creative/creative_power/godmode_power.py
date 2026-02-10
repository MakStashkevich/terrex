from dataclasses import dataclass
from terrex.structures.game_content.creative.creative_power.creative_power import CreativePower
from terrex.util.streamer import Reader, Writer

 

@dataclass()
class GodmodePower(CreativePower):
    id: int = 5
    enabled: bool | None = None

    @classmethod
    def create(cls, enabled: bool = False) -> "GodmodePower":
        obj = cls()
        obj.enabled = enabled
        return obj

    def read(self, reader: Reader) -> None:
        self.enabled = reader.read_bool()

    def write(self, writer: Writer) -> None:
        writer.write_bool(self.enabled)
