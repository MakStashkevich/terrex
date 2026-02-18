from dataclasses import dataclass

from terrex.net.ambience.sky_entity_type import SkyEntityType
from terrex.net.streamer import Reader, Writer

from .net_module import NetServerModule


@dataclass()
class NetAmbienceModule(NetServerModule):
    id: int = 3
    player_id: int | None = None
    rand_next_num: int | None = None
    sky_entity_type: SkyEntityType | None = None

    @classmethod
    def create(cls, player_id: int, rand_next_num: int, sky_entity_type: SkyEntityType) -> "NetAmbienceModule":
        obj = cls()
        obj.player_id = player_id
        obj.rand_next_num = rand_next_num
        obj.sky_entity_type = sky_entity_type
        return obj

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.rand_next_num = reader.read_int()
        self.sky_entity_type = SkyEntityType(reader.read_byte())

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_int(self.rand_next_num)
        writer.write_byte(self.sky_entity_type.value)
