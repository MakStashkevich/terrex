from dataclasses import dataclass, field

from terrex.item.item import Item
from terrex.net.streamer import Reader, Writer


@dataclass
class Chest:
    index: int = 0
    x: int = 0
    y: int = 0
    name: str = ""
    max_items: int = 40
    bank_chest: bool = False
    items: list[Item] = field(default_factory=list)
    _items_got_set: bool = False

    @classmethod
    def create(
        cls, index: int = 0, x: int = 0, y: int = 0, bank: bool = False, max_items: int = 40
    ) -> 'Chest':
        chest = cls(index=index, x=x, y=y, bank_chest=bank, max_items=max_items)
        chest.fill_with_empty_instances()
        return chest

    @classmethod
    def read(cls, reader: Reader) -> 'Chest':
        chest = cls(
            reader.read_short(),
            reader.read_short(),
            reader.read_short(),
            reader.read_dotnet_string(),
        )
        chest.fill_with_empty_instances()
        return chest

    def write(self, writer: Writer) -> None:
        writer.write_short(self.index)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_dotnet_string(self.name)

    def fill_with_empty_instances(self) -> None:
        self.items = [Item() for _ in range(self.max_items)]
        self._items_got_set = True
