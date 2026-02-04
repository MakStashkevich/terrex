import struct

class Reader:
    """Чтение данных из байтового буфера Terraria протокола."""
    def __init__(self, data: bytes):
        self.data = data
        self.index = 0

    def read_byte(self) -> int:
        res = self.data[self.index]
        self.index += 1
        return res

    def read_short(self) -> int:
        res = struct.unpack("<h", self.data[self.index:self.index+2])[0]
        self.index += 2
        return res

    def read_ushort(self) -> int:
        res = struct.unpack("<H", self.data[self.index:self.index+2])[0]
        self.index += 2
        return res

    def read_int(self) -> int:
        res = struct.unpack("<i", self.data[self.index:self.index+4])[0]
        self.index += 4
        return res

    def read_float(self) -> float:
        res = struct.unpack("<f", self.data[self.index:self.index+4])[0]
        self.index += 4
        return res

    def read_string(self) -> str:
        length = self.read_byte()
        if length == 0:
            return ""
        res = self.data[self.index:self.index + length].decode("utf-8")
        self.index += length
        return res

    def read_bytes(self, length: int) -> bytes:
        res = self.data[self.index:self.index + length]
        self.index += length
        return res

    def remaining(self) -> bytes:
        return self.data[self.index:]

    def eof(self) -> bool:
        return self.index >= len(self.data)

class Writer:
    """Запись данных в байтовый буфер Terraria протокола."""
    def __init__(self):
        self.data = bytearray()

    def write_byte(self, value: int):
        self.data.append(value & 0xFF)

    def write_short(self, value: int):
        self.data.extend(struct.pack("<h", value))

    def write_ushort(self, value: int):
        self.data.extend(struct.pack("<H", value))

    def write_int(self, value: int):
        self.data.extend(struct.pack("<i", value))

    def write_float(self, value: float):
        self.data.extend(struct.pack("<f", value))

    def write_string(self, value: str):
        b = value.encode("utf-8")
        if len(b) > 127:
            raise ValueError("Pascal string too long (max 127 bytes)")
        self.write_byte(len(b))
        self.data.extend(b)

    def write_bytes(self, value: bytes):
        self.data.extend(value)

    def bytes(self) -> bytes:
        return bytes(self.data)
