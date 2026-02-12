from dataclasses import dataclass
from terrex.structures.chat.chat_command import ChatCommand
from terrex.structures.net_mode import NetMode
from terrex.structures.localization.network_text import NetworkText
from terrex.structures.rgb import Rgb
from terrex.util.streamer import Reader, Writer
from .net_module import NetSyncModule


@dataclass()
class NetTextModule(NetSyncModule):
    id: int = 1
    chat_command_id: ChatCommand | None = None
    author_id: int | None = None
    text: NetworkText | None = None
    color: Rgb | None = None

    @classmethod
    def create(cls, author_id: int, text: NetworkText, color: Rgb) -> "NetTextModule":
        obj = cls()
        obj.author_id = author_id
        obj.text = text
        obj.color = color
        return obj

    def read(self, reader: Reader) -> None:
        if reader.net_mode == NetMode.CLIENT:
            self.chat_command_id = ChatCommand(reader.read_dotnet_string())
            self.text = reader.read_dotnet_string()
        else:
            self.author_id = reader.read_byte()
            self.text = NetworkText.read(reader)
            self.color = Rgb.read(reader)

    def write(self, writer: Writer) -> None:
        if writer.net_mode == NetMode.CLIENT:
            writer.write_dotnet_string(self.chat_command_id)
            writer.write_dotnet_string(self.text)
        else:
            writer.write_byte(self.author_id)
            self.text.write(writer)
            self.color.write(writer)
