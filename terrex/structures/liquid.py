from dataclasses import dataclass
from terrex.util.streamer import Reader, Writer
from terrex.structures.liquid_type import LiquidType

@dataclass
class Liquid:
    y: int
    x: int
    amount: int
    ty: LiquidType

    @classmethod
    def read(cls, reader: Reader) -> 'Liquid':
        return cls(
            reader.read_short(),
            reader.read_short(),
            reader.read_byte(),
            LiquidType.read(reader)
        )

    def write(self, writer: Writer) -> None:
        writer.write_short(self.y)
        writer.write_short(self.x)
        writer.write_byte(self.amount)
        self.ty.write(writer)