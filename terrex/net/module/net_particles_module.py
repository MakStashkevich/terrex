from dataclasses import dataclass

from terrex.net.drawing.particle_orchestra_settings import ParticleOrchestraSettings
from terrex.net.streamer import Reader, Writer

from .net_module import NetSyncModule


@dataclass()
class NetParticlesModule(NetSyncModule):
    id: int = 8
    particle_orchestra_type: int = 0
    particle_orchestra_settings: ParticleOrchestraSettings | None = None

    @classmethod
    def create(
        cls, particle_orchestra_type: int, particle_orchestra_settings: ParticleOrchestraSettings
    ) -> "NetParticlesModule":
        obj = cls()
        obj.particle_orchestra_type = particle_orchestra_type
        obj.particle_orchestra_settings = particle_orchestra_settings
        return obj

    def read(self, reader: Reader) -> None:
        self.particle_orchestra_type = reader.read_byte()
        self.particle_orchestra_settings = ParticleOrchestraSettings.read(reader)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.particle_orchestra_type)
        if self.particle_orchestra_settings is None:
            raise ValueError("particle_orchestra_settings must not be None")
        self.particle_orchestra_settings.write(writer)
