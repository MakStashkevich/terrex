from typing import List
from terrex.util.streamer import Reader, Writer
from .base import NetServerModule


class NetCraftingRequestModule(NetServerModule):
    def __init__(self, items: list[tuple[int, int]], chests: list[int | None]):
        self.items = items  # (item_id, stack)
        self.chests = chests  # chest.index or None (-1)

    @classmethod
    def read(cls, reader: Reader) -> 'NetCraftingRequestModule':
        num_items = reader.read_7bit_encoded_int()
        items = []
        for _ in range(num_items):
            item_id = reader.read_int()
            stack = reader.read_7bit_encoded_int()
            items.append((item_id, stack))
        num_chests = reader.read_7bit_encoded_int()
        chests = []
        for _ in range(num_chests):
            idx = reader.read_7bit_encoded_int()
            chests.append(None if idx < 0 else idx)
        return cls(items, chests)

    def write(self, writer: Writer) -> None:
        writer.write_7bit_encoded_int(len(self.items))
        for item_id, stack in self.items:
            writer.write_int(item_id)
            writer.write_7bit_encoded_int(stack)
        writer.write_7bit_encoded_int(len(self.chests))
        for chest in self.chests:
            idx = -1 if chest is None else chest
            writer.write_7bit_encoded_int(idx)
