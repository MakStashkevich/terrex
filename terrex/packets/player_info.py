from typing import Tuple
from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer

class PlayerInfo(Packet):
    id = PacketIds.PLAYER_INFO.value

    def __init__(self, name: str = "", hair: int = 0,
                 skin_color: Tuple[int, int, int] = (0, 0, 0),
                 hair_color: Tuple[int, int, int] = (0, 0, 0),
                 eye_color: Tuple[int, int, int] = (0, 0, 0),
                 shirt_color: Tuple[int, int, int] = (0, 0, 0),
                 undershirt_color: Tuple[int, int, int] = (0, 0, 0),
                 pants_color: Tuple[int, int, int] = (0, 0, 0),
                 shoes_color: Tuple[int, int, int] = (0, 0, 0)):
        self.name = name
        self.hair = hair
        self.skin_color = skin_color
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.shirt_color = shirt_color
        self.undershirt_color = undershirt_color
        self.pants_color = pants_color
        self.shoes_color = shoes_color

    def _read_color(self, reader: Reader) -> Tuple[int, int, int]:
        return (reader.read_byte(), reader.read_byte(), reader.read_byte())

    def _write_color(self, writer: Writer, color: Tuple[int, int, int]):
        writer.write_byte(color[0])
        writer.write_byte(color[1])
        writer.write_byte(color[2])

    def read(self, reader: Reader):
        self.name = reader.read_string()
        self.hair = reader.read_byte()
        self.skin_color = self._read_color(reader)
        self.hair_color = self._read_color(reader)
        self.eye_color = self._read_color(reader)
        self.shirt_color = self._read_color(reader)
        self.undershirt_color = self._read_color(reader)
        self.pants_color = self._read_color(reader)
        self.shoes_color = self._read_color(reader)

    def write(self, writer: Writer):
        writer.write_string(self.name)
        writer.write_byte(self.hair)
        self._write_color(writer, self.skin_color)
        self._write_color(writer, self.hair_color)
        self._write_color(writer, self.eye_color)
        self._write_color(writer, self.shirt_color)
        self._write_color(writer, self.undershirt_color)
        self._write_color(writer, self.pants_color)
        self._write_color(writer, self.shoes_color)

PlayerInfo.register()