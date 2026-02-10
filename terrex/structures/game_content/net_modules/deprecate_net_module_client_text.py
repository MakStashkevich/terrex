from dataclasses import dataclass
from terrex.util.streamer import Reader, Writer
from .net_module import NetClientModule


@dataclass()
class LoadNetModuleClientText(NetClientModule):
    id: int = 0
    command: str | None = None
    text: str | None = None

    @classmethod
    def create(cls, command: str, text: str) -> "LoadNetModuleClientText":
        obj = cls()
        obj.command = command
        obj.text = text
        return obj

    def read(self, reader: Reader) -> None:
        raise NotImplementedError("NetClientModule does not implement read")

    def write(self, writer: Writer) -> None:
        writer.write_string(self.command)
        writer.write_string(self.text)
