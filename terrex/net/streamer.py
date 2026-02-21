import struct

from terrex.net.enum.mode import NetMode


class Reader:
    """Reading data from Terraria protocol byte buffer."""

    def __init__(self, data: bytes, protocol_version: int = 0, net_mode: NetMode = NetMode.SERVER):
        """Initializes the reader with byte data."""
        self.data = data
        self.index = 0
        self.version = protocol_version
        self.net_mode = net_mode

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
        res = struct.unpack("<b", self.data[self.index : self.index + 1])[0]
        self.index += 1
        return res

    def read_short(self) -> int:
        """Reads a signed 16-bit integer (short, int16, little-endian)."""
        if self.index + 2 > len(self.data):
            raise ValueError(f"Cannot read short: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<h", self.data[self.index : self.index + 2])[0]
        self.index += 2
        return res

    def read_ushort(self) -> int:
        """Reads an unsigned 16-bit integer (ushort, uint16, little-endian)."""
        if self.index + 2 > len(self.data):
            raise ValueError(f"Cannot read ushort: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<H", self.data[self.index : self.index + 2])[0]
        self.index += 2
        return res

    def read_int(self) -> int:
        """Reads a signed 32-bit integer (int, int32, little-endian)."""
        if self.index + 4 > len(self.data):
            raise ValueError(f"Cannot read int: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<i", self.data[self.index : self.index + 4])[0]
        self.index += 4
        return res

    def read_ulong(self) -> int:
        """Reads an unsigned 64-bit integer (ulong, uint64, little-endian)."""
        if self.index + 8 > len(self.data):
            raise ValueError(f"Cannot read ulong: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<Q", self.data[self.index : self.index + 8])[0]
        self.index += 8
        return res

    def read_float(self) -> float:
        """Reads a 32-bit IEEE 754 float (little-endian)."""
        if self.index + 4 > len(self.data):
            raise ValueError(f"Cannot read float: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<f", self.data[self.index : self.index + 4])[0]
        self.index += 4
        return res

    def read_single(self) -> float:
        """Reads a 32-bit IEEE 754 float (Single, little-endian)."""
        if self.index + 4 > len(self.data):
            raise ValueError(f"Cannot read single: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack_from("<f", self.data, self.index)[0]
        self.index += 4
        return res

    def read_double(self) -> float:
        """Reads a 64-bit IEEE 754 double (little-endian)."""
        if self.index + 8 > len(self.data):
            raise ValueError(f"Cannot read double: only {len(self.data) - self.index} bytes remaining")
        res = struct.unpack("<d", self.data[self.index : self.index + 8])[0]
        self.index += 8
        return res

    def read_7bit_encoded_int(reader) -> int:
        """Reads a .NET 7-bit encoded int (variable-length)."""
        value = 0
        shift = 0

        while True:
            b = reader.read_byte()
            value |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7
        return value

    # BinaryReader.ReadString()
    def read_dotnet_string(self) -> str:
        """Reads a Terraria string: 7-bit varint length."""
        length = self.read_7bit_encoded_int()
        data = self.read_bytes(length)
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return repr(data)

    def read_bytes(self, length: int) -> bytes:
        """Reads the specified number of raw bytes."""
        if self.index + length > len(self.data):
            raise ValueError("Not enough bytes remaining")
        res = self.data[self.index : self.index + length]
        self.index += length
        return res

    def remaining(self) -> bytes:
        """Returns the remaining unread bytes."""
        return self.data[self.index :]

    def eof(self) -> bool:
        """Checks if the end of data has been reached."""
        return self.index >= len(self.data)

    def read_bool(self) -> bool:
        """Reads a byte interpreted as boolean (non-zero = true)."""
        return bool(self.read_byte())


class Writer:
    """Writing data to Terraria protocol byte buffer."""

    def __init__(self, protocol_version: int = 0, net_mode: NetMode = NetMode.CLIENT):
        """Initializes the writer with an empty bytearray."""
        self.data = bytearray()
        self.version = protocol_version
        self.net_mode = net_mode

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

    def write_single(self, value: float):
        """Writes a 32-bit IEEE 754 float (Single, little-endian)."""
        self.data.extend(struct.pack("<f", value))

    def write_double(self, value: float):
        """Writes a 64-bit IEEE 754 double (little-endian)."""
        self.data.extend(struct.pack("<d", value))

    def write_7bit_encoded_int(self, value: int):
        """Writes a .NET 7-bit encoded int (variable-length)."""
        if value < 0:
            raise ValueError("7-bit encoded int must be non-negative")
        while value >= 0x80:
            self.write_byte((value & 0x7F) | 0x80)
            value >>= 7
        self.write_byte(value & 0x7F)

    def write_dotnet_string(self, text: str) -> bytes:
        """Writes a Terraria string: 7-bit varint length."""
        raw = text.encode("utf-8")
        self.write_7bit_encoded_int(len(raw))
        for b in raw:
            self.write_byte(b)

    def write_bytes(self, value: bytes):
        """Writes raw bytes."""
        self.data.extend(value)

    def write_bool(self, value: bool):
        """Writes a boolean as a byte (1 for true, 0 for false)."""
        self.write_byte(1 if value else 0)

    def bytes(self) -> bytes:
        """Returns the final bytes of the written data."""
        return bytes(self.data)
