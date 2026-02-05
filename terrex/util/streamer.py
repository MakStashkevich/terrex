import struct

class Reader:
    """Reading data from Terraria protocol byte buffer."""
    def __init__(self, data: bytes):
        """Initializes the reader with byte data."""
        self.data = data
        self.index = 0

    def read_byte(self) -> int:
        """Reads an unsigned 8-bit integer (byte, uint8)."""
        if self.index >= len(self.data):
            raise ValueError("Cannot read byte: no data remaining")
        res = self.data[self.index]
        self.index += 1
        return res

    def read_sbyte(self) -> int:
        """Reads a signed 8-bit integer (sbyte, int8, little-endian)."""
        if self.index + 1 > len(self.data):
            raise ValueError(f"Cannot read sbyte: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<b", self.data[self.index:self.index+1])[0]
        self.index += 1
        return res

    def read_short(self) -> int:
        """Reads a signed 16-bit integer (short, int16, little-endian)."""
        if self.index + 2 > len(self.data):
            raise ValueError(f"Cannot read short: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<h", self.data[self.index:self.index+2])[0]
        self.index += 2
        return res

    def read_ushort(self) -> int:
        """Reads an unsigned 16-bit integer (ushort, uint16, little-endian)."""
        if self.index + 2 > len(self.data):
            raise ValueError(f"Cannot read ushort: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<H", self.data[self.index:self.index+2])[0]
        self.index += 2
        return res

    def read_int(self) -> int:
        """Reads a signed 32-bit integer (int, int32, little-endian)."""
        if self.index + 4 > len(self.data):
            raise ValueError(f"Cannot read int: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<i", self.data[self.index:self.index+4])[0]
        self.index += 4
        return res

    def read_ulong(self) -> int:
        """Reads an unsigned 64-bit integer (ulong, uint64, little-endian)."""
        if self.index + 8 > len(self.data):
            raise ValueError(f"Cannot read ulong: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<Q", self.data[self.index:self.index+8])[0]
        self.index += 8
        return res

    def read_float(self) -> float:
        """Reads a 32-bit IEEE 754 float (little-endian)."""
        if self.index + 4 > len(self.data):
            raise ValueError(f"Cannot read float: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<f", self.data[self.index:self.index+4])[0]
        self.index += 4
        return res

    def read_string(self) -> str:
        """Reads a Pascal string: 1-byte length (0-127) followed by UTF-8 bytes."""
        length = self.read_byte()
        if length == 0:
            return ""
        res = self.data[self.index:self.index + length].decode("utf-8")
        self.index += length
        return res

    def read_bytes(self, length: int) -> bytes:
        """Reads the specified number of raw bytes."""
        res = self.data[self.index:self.index + length]
        self.index += length
        return res

    def remaining(self) -> bytes:
        """Returns the remaining unread bytes."""
        return self.data[self.index:]

    def eof(self) -> bool:
        """Checks if the end of data has been reached."""
        return self.index >= len(self.data)

    def read_bool(self) -> bool:
        """Reads a byte interpreted as boolean (non-zero = true)."""
        return bool(self.read_byte())
    
class Writer:
    """Writing data to Terraria protocol byte buffer."""
    def __init__(self):
        """Initializes the writer with an empty bytearray."""
        self.data = bytearray()

    def write_byte(self, value: int):
        """Writes an unsigned 8-bit integer (byte, uint8)."""
        self.data.append(value & 0xFF)

    def write_sbyte(self, value: int):
        """Writes a signed 8-bit integer (sbyte, int8, little-endian)."""
        self.data.extend(struct.pack("<b", value))

    def write_short(self, value: int):
        """Writes a signed 16-bit integer (short, int16, little-endian)."""
        self.data.extend(struct.pack("<h", value))

    def write_ushort(self, value: int):
        """Writes an unsigned 16-bit integer (ushort, uint16, little-endian)."""
        self.data.extend(struct.pack("<H", value))

    def write_int(self, value: int):
        """Writes a signed 32-bit integer (int, int32, little-endian)."""
        self.data.extend(struct.pack("<i", value))

    def write_ulong(self, value: int):
        """Writes an unsigned 64-bit integer (ulong, uint64, little-endian)."""
        self.data.extend(struct.pack("<Q", value))

    def write_float(self, value: float):
        """Writes a 32-bit IEEE 754 float (little-endian)."""
        self.data.extend(struct.pack("<f", value))

    def write_string(self, value: str):
        """Writes a Pascal string: 1-byte length (0-127) followed by UTF-8 bytes."""
        b = value.encode("utf-8")
        if len(b) > 127:
            raise ValueError("Pascal string too long (max 127 bytes)")
        self.write_byte(len(b))
        self.data.extend(b)

    def write_bytes(self, value: bytes):
        """Writes raw bytes."""
        self.data.extend(value)

    def write_bool(self, value: bool):
        """Writes a boolean as a byte (1 for true, 0 for false)."""
        self.write_byte(1 if value else 0)

    def bytes(self) -> bytes:
        """Returns the final bytes of the written data."""
        return bytes(self.data)
