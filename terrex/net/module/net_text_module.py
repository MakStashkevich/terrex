from dataclasses import dataclass

from terrex.localization.network_text import NetworkText
from terrex.net.enum.chat_command import ChatCommand
from terrex.net.enum.mode import NetMode
from terrex.net.streamer import Reader, Writer
from terrex.net.structure.rgb import Rgb

from .net_module import NetSyncModule


@dataclass()
class NetTextModule(NetSyncModule):
    id: int = 1
    chat_command_id: ChatCommand | None = None
    author_id: int | None = None
    text: str | None = None
    net_text: NetworkText | None = None
    color: Rgb | None = None

    @classmethod
    def create(
        cls,
        chat_command_id: ChatCommand,
        author_id: int | None = None,
        text: str | None = None,
        net_text: NetworkText | None = None,
        color: Rgb | None = None,
    ) -> "NetTextModule":
        obj = cls()
        obj.chat_command_id = chat_command_id
        obj.author_id = author_id
        obj.text = text
        obj.net_text = net_text
        obj.color = color
        return obj

    def read(self, reader: Reader) -> None:
        if reader.net_mode == NetMode.CLIENT:
            self.chat_command_id = ChatCommand(reader.read_dotnet_string())
            self.text = reader.read_dotnet_string()
        else:
            self.author_id = reader.read_byte()
            self.net_text = NetworkText.read(reader)
            self.color = Rgb.read(reader)

    def write(self, writer: Writer) -> None:
        if writer.net_mode == NetMode.CLIENT:
            if self.chat_command_id is None or self.text is None:
                raise ValueError("chat_command_id and text_str must not be None in CLIENT mode")
            writer.write_dotnet_string(str(self.chat_command_id))
            writer.write_dotnet_string(self.text)
        else:
            if self.author_id is None or self.net_text is None or self.color is None:
                raise ValueError("author_id, net_text, color must not be None in SERVER mode")
            writer.write_byte(self.author_id)
            self.net_text.write(writer)
            self.color.write(writer)
