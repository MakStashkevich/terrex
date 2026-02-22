from re import Match
from typing import Any, List

from terrex.net.enum.chat_command import ChatCommand


class BaseEvent:
    def __init__(self, packet):
        from terrex.packet import Packet

        if not isinstance(packet, Packet):
            raise TypeError("packet must be a Packet instance")

        self.packet = packet


class RegexEvent(BaseEvent):
    pattern_match: Match[str] | None = None


class LoginEvent(BaseEvent):
    def __init__(self, packet):
        super().__init__(packet)


class PlayerIDEvent(BaseEvent):
    def __init__(self, packet, player_id: int):
        super().__init__(packet)
        self.player_id: int = player_id


class BlockedEvent(BaseEvent):
    def __init__(self, packet, reason: str):
        super().__init__(packet)
        self.reason: str = reason


class InitializedEvent(BaseEvent):
    def __init__(self, packet):
        super().__init__(packet)


class ChatEvent(RegexEvent):
    def __init__(self, packet, player_id: int, text: str, chat_command_id: ChatCommand):
        super().__init__(packet)
        self.player_id: int = player_id
        self.text: str = text
        self.chat_command_id: ChatCommand = chat_command_id


class TileSectionUpdateEvent(BaseEvent):
    def __init__(self, packet, tiles: List[Any]):
        super().__init__(packet)
        self.tiles: List[Any] = tiles


class ItemOwnerChangedEvent(BaseEvent):
    def __init__(self, packet, item_id: int, player_id: int):
        super().__init__(packet)
        self.item_id: int = item_id
        self.player_id: int = player_id


class ItemEvent(BaseEvent):
    def __init__(self, packet, item):
        super().__init__(packet)

        from terrex.item.item import Item

        if not isinstance(item, Item):
            raise TypeError("item must be a Item instance")

        self.item: Item = item


class ItemDroppedEvent(ItemEvent):
    pass


class ItemDropUpdateEvent(ItemEvent):
    pass
