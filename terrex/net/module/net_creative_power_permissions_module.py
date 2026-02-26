from dataclasses import dataclass

from terrex.net.streamer import Reader, Writer

from .net_module import NetServerModule


@dataclass()
class NetCreativePowerPermissionsModule(NetServerModule):
    id: int = 9
    zero: int = 0
    power_id: int = 0
    level: int = 0

    @classmethod
    def create(cls, zero: int, power_id: int, level: int) -> "NetCreativePowerPermissionsModule":
        obj = cls()
        obj.zero = zero
        obj.power_id = power_id
        obj.level = level
        return obj

    def read(self, reader: Reader) -> None:
        self.zero = reader.read_byte()
        if self.zero == 0:
            self.power_id = reader.read_ushort()
            self.level = reader.read_byte()

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.zero)
        writer.write_ushort(self.power_id)
        writer.write_byte(self.level)
