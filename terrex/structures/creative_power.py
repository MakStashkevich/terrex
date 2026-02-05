from dataclasses import dataclass
from typing import Optional
from terrex.util.streamer import Reader, Writer

@dataclass
class CreativePower:
    variant: int  # 0-14
    # Common fields
    val_i16: Optional[int] = None
    val_u8_ty: Optional[int] = None
    val_i16_left: Optional[int] = None
    val_i16_right: Optional[int] = None
    val_i32: Optional[int] = None
    data_32: Optional[bytes] = None
    data_6: Optional[bytes] = None

    @classmethod
    def read(cls, reader: Reader) -> 'CreativePower':
        variant = reader.read_byte()
        cp = cls(variant=variant)
        if variant == 0:
            cp.val_i16 = reader.read_short()
        elif variant == 1:
            pass  # StartDayImmediately
        elif variant == 2:
            pass  # StartNoonImmediately
        elif variant == 3:
            pass  # StartNightImmediately
        elif variant == 4:
            pass  # StartMidnightImmediately
        elif variant == 5:
            cp.val_i16 = reader.read_short()
            cp.data_32 = reader.read_bytes(32)
        elif variant == 6:
            pass  # ModifyWindDirectionAndStrength
        elif variant == 7:
            pass  # ModifyRainPower
        elif variant == 8:
            cp.val_u8_ty = reader.read_byte()
            cp.val_i16_left = reader.read_short()
            cp.val_i16_right = reader.read_short()
        elif variant == 9:
            cp.val_i16 = reader.read_short()
        elif variant == 10:
            cp.val_i16 = reader.read_short()
        elif variant == 11:
            cp.val_i16 = reader.read_short()
            cp.data_32 = reader.read_bytes(32)
        elif variant == 12:
            cp.val_u8_ty = reader.read_byte()
            cp.val_i32 = reader.read_int()
        elif variant == 13:
            cp.val_i16 = reader.read_short()
        elif variant == 14:
            cp.data_6 = reader.read_bytes(6)
        else:
            raise ValueError(f"Unknown CreativePower variant: {variant}")
        return cp

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.variant)
        if self.variant == 0:
            assert self.val_i16 is not None
            writer.write_short(self.val_i16)
        elif self.variant == 5:
            assert self.val_i16 is not None and self.data_32 is not None
            writer.write_short(self.val_i16)
            writer.write_bytes(self.data_32)
        elif self.variant == 8:
            assert self.val_u8_ty is not None and self.val_i16_left is not None and self.val_i16_right is not None
            writer.write_byte(self.val_u8_ty)
            writer.write_short(self.val_i16_left)
            writer.write_short(self.val_i16_right)
        elif self.variant == 9:
            assert self.val_i16 is not None
            writer.write_short(self.val_i16)
        elif self.variant == 10:
            assert self.val_i16 is not None
            writer.write_short(self.val_i16)
        elif self.variant == 11:
            assert self.val_i16 is not None and self.data_32 is not None
            writer.write_short(self.val_i16)
            writer.write_bytes(self.data_32)
        elif self.variant == 12:
            assert self.val_u8_ty is not None and self.val_i32 is not None
            writer.write_byte(self.val_u8_ty)
            writer.write_int(self.val_i32)
        elif self.variant == 13:
            assert self.val_i16 is not None
            writer.write_short(self.val_i16)
        elif self.variant == 14:
            assert self.data_6 is not None
            writer.write_bytes(self.data_6)
        # Other variants have no data