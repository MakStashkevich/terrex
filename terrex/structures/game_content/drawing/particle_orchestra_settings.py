from dataclasses import dataclass

from terrex.structures.vec2 import Vec2
from terrex.util.streamer import Reader, Writer


@dataclass
class ParticleOrchestraSettings:
    position_in_world: Vec2
    movement_vector: Vec2
    unique_info_piece: int
    index_of_player_who_invoked_this: int

    @classmethod
    def read(cls, reader: Reader) -> 'ParticleOrchestraSettings':
        return cls(Vec2.read(reader), Vec2.read(reader), reader.read_int(), reader.read_byte())

    def write(self, writer: Writer) -> None:
        self.position_in_world.write(writer)
        self.movement_vector.write(writer)
        writer.write_int(self.unique_info_piece)
        writer.write_byte(self.index_of_player_who_invoked_this)
