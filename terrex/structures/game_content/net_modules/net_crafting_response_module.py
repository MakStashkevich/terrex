from dataclasses import dataclass
from terrex.util.streamer import Reader, Writer
from .net_module import NetClientModule

@dataclass()
class NetCraftingResponseModule(NetClientModule):
    id: int = 11
    approved: bool | None = None

    @classmethod
    def create(cls, approved: bool) -> 'NetCraftingResponseModule':
        obj = cls()
        obj.approved = approved
        return obj

    def read(self, reader: Reader) -> None:
        raise NotImplementedError("NetClientModule does not implement read")

    def write(self, writer: Writer) -> None:
        writer.write_bool(self.approved)
