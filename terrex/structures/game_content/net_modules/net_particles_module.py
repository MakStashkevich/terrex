from terrex.structures.game_content.drawing.particle_orchestra_settings import ParticleOrchestraSettings
from terrex.util.streamer import Reader, Writer
from .base import NetSyncModule


class NetParticlesModule(NetSyncModule):
    def __init__(self, particle_orchestra_type: int, particle_orchestra_settings: ParticleOrchestraSettings):
        self.particle_orchestra_type = particle_orchestra_type
        self.particle_orchestra_settings = particle_orchestra_settings

    @classmethod
    def read(cls, reader: Reader) -> 'NetParticlesModule':
        particle_orchestra_type = reader.read_byte()
        particle_orchestra_settings = ParticleOrchestraSettings.read(reader)
        return cls(particle_orchestra_type, particle_orchestra_settings)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.particle_orchestra_type)
        self.particle_orchestra_settings.write(writer)
