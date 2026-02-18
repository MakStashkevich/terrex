from enum import IntFlag

from terrex.packet.base import ClientPacket
from terrex.id import MessageID
from terrex.net.streamer import Reader, Writer


class ToolMode(IntFlag):
    RED = 0x01
    GREEN = 0x02
    BLUE = 0x04
    YELLOW = 0x08
    ACTUATOR = 0x10
    CUTTER = 0x20

    @classmethod
    def read(cls, reader: Reader) -> 'ToolMode':
        return cls(reader.read_byte())

    def write(self, writer: Writer):
        writer.write_byte(self.value)


class MassWireOperation(ClientPacket):
    id = MessageID.MassWireOperation

    def __init__(self, start_x: int = 0, start_y: int = 0, end_x: int = 0, end_y: int = 0, tool_mode: ToolMode = ToolMode.RED):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.tool_mode = tool_mode

    def read(self, reader: Reader):
        self.start_x = reader.read_short()
        self.start_y = reader.read_short()
        self.end_x = reader.read_short()
        self.end_y = reader.read_short()
        self.tool_mode = ToolMode.read(reader)

    def write(self, writer: Writer):
        writer.write_short(self.start_x)
        writer.write_short(self.start_y)
        writer.write_short(self.end_x)
        writer.write_short(self.end_y)
        self.tool_mode.write(writer)
