from typing import Any

from terrex.packets.base import Packet
from terrex.packets.packet_ids import PacketIds
from terrex.util.streamer import Reader, Writer


class Time(Packet):
    id = PacketIds.TIME.value

    def __init__(self, day_time: bool = False, time: int = 0, sun_mod_y: int = 0, moon_mod_y: int = 0):
        self.day_time = day_time
        self.time = time
        self.sun_mod_y = sun_mod_y
        self.moon_mod_y = moon_mod_y

    def read(self, reader: Reader):
        self.day_time = reader.read_bool()
        self.time = reader.read_int()
        self.sun_mod_y = reader.read_short()
        self.moon_mod_y = reader.read_short()

    def write(self, writer: Writer):
        writer.write_bool(self.day_time)
        writer.write_int(self.time)
        writer.write_short(self.sun_mod_y)
        writer.write_short(self.moon_mod_y)

Time.register()