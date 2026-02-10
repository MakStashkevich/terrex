from dataclasses import dataclass
from terrex.util.streamer import Reader, Writer
from .liquid_type import LiquidType

@dataclass
class Liquid:
    x: int
    y: int
    amount: int
    type: LiquidType

    @classmethod
    def read(cls, reader: Reader) -> 'Liquid':
        pos = reader.read_int()
        amount = reader.read_byte()
        type = LiquidType.read(reader)
        x = (pos >> 16) & 0xFFFF
        y = pos & 0xFFFF
        return cls(x, y, amount, type)

    def write(self, writer: Writer) -> None:
        pos = (self.x << 16) | self.y
        writer.write_int(pos)
        writer.write_byte(self.amount)
        self.type.write(writer)