from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class NetCreativePowerPermissionsModule(NetServerModule):
    def __init__(self, zero: int, power_id: int, level: int):
        self.zero = zero
        self.power_id = power_id
        self.level = level

    @classmethod
    def read(cls, reader: Reader) -> 'NetCreativePowerPermissionsModule':
        zero = reader.read_byte()
        if zero == 0:
            power_id = reader.read_ushort()
            level = reader.read_byte()
        return cls(zero, power_id, level)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.zero)
        writer.write_ushort(self.power_id)
        writer.write_byte(self.level)
