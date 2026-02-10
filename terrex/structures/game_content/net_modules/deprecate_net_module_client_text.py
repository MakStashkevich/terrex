from terrex.util.streamer import Reader, Writer
from .base import NetClientModule


class LoadNetModuleClientText(NetClientModule):
    def __init__(self, command: str, text: str):
        self.command = command
        self.text = text

    @classmethod
    def read(cls, reader: Reader) -> 'LoadNetModuleClientText':
        # Fallback read, may not be accurate
        command = reader.read_string()
        text = reader.read_string()
        return cls(command, text)

    def write(self, writer: Writer) -> None:
        writer.write_string(self.command)
        writer.write_string(self.text)
