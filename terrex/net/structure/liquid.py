from dataclasses import dataclass

from terrex.id import LiquidID
from terrex.net.streamer import Reader, Writer


@dataclass
class Liquid:
    x: int
    y: int
    amount: int
    type: LiquidID

    @classmethod
    def read(cls, reader: Reader) -> 'Liquid':
        pos = reader.read_int()
        amount = reader.read_byte()
        type = LiquidID(reader.read_byte())
        x = (pos >> 16) & 0xFFFF
        y = pos & 0xFFFF
        return cls(x, y, amount, type)

    def write(self, writer: Writer) -> None:
        pos = (self.x << 16) | self.y
        writer.write_int(pos)
        writer.write_byte(self.amount)
        writer.write_byte(self.type)
