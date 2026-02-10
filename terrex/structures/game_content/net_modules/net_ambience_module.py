from terrex.structures.game_content.ambience.sky_entity_type import SkyEntityType
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class NetAmbienceModule(NetServerModule):
    def __init__(self, player_id: int, rand_next_num: int, sky_entity_type: SkyEntityType):
        self.player_id = player_id
        self.rand_next_num = rand_next_num
        self.sky_entity_type = sky_entity_type

    @classmethod
    def read(cls, reader: Reader) -> 'NetAmbienceModule':
        player_id = reader.read_byte()
        rand_next_num = reader.read_int()
        sky_entity_type = SkyEntityType(reader.read_byte())
        return cls(player_id, rand_next_num, sky_entity_type)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_int(self.rand_next_num)
        writer.write_byte(self.sky_entity_type.value)
