from dataclasses import dataclass
from typing import List, Tuple
from terrex.util.streamer import Reader, Writer
from .net_module import NetServerModule

@dataclass()
class NetCraftingRequestModule(NetServerModule):
    id: int = 11
    items: List[Tuple[int, int]] | None = None
    chests: List[int | None] | None = None

    @classmethod
    def create(cls, items: List[Tuple[int, int]], chests: List[int | None]) -> 'NetCraftingRequestModule':
        obj = cls()
        obj.items = items
        obj.chests = chests
        return obj

    def read(self, reader: Reader) -> None:
        num_items = reader.read_7bit_encoded_int()
        self.items = []
        for _ in range(num_items):
            item_id = reader.read_int()
            stack = reader.read_7bit_encoded_int()
            self.items.append((item_id, stack))
        num_chests = reader.read_7bit_encoded_int()
        self.chests = []
        for _ in range(num_chests):
            idx = reader.read_7bit_encoded_int()
            self.chests.append(None if idx < 0 else idx)

    def write(self, writer: Writer) -> None:
        writer.write_7bit_encoded_int(len(self.items))
        for item_id, stack in self.items:
            writer.write_int(item_id)
            writer.write_7bit_encoded_int(stack)
        writer.write_7bit_encoded_int(len(self.chests))
        for chest in self.chests:
            idx = -1 if chest is None else chest
            writer.write_7bit_encoded_int(idx)
