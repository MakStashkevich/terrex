from re import Match
from typing import Any


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
    def __init__(self, packet, player_id: int, text: str, chat_command_id: Any | None = None):
        super().__init__(packet)
        from terrex.net.enum.chat_command import ChatCommand

        self.player_id: int = player_id
        self.text: str = text
        self.chat_command_id: ChatCommand | None = chat_command_id


class WorldSectionUpdateEvent(BaseEvent):
    def __init__(self, packet, section):
        super().__init__(packet)

        from terrex.net.structure.world_section import WorldSection

        if not isinstance(section, WorldSection):
            return

        self.section = section


class PlayerControlUpdateEvent(BaseEvent):
    def __init__(
        self,
        packet,
        player_id: int,
        control,
        selected_item_id: int,
        position,
        velocity,
        mount_type: int,
        potion_of_return_original_use_position,
        potion_of_return_home_position,
        net_camera_target,
    ):
        super().__init__(packet)
        from terrex.net.player_control import PlayerControl
        from terrex.net.structure.vec2 import Vec2

        self.player_id: int = player_id
        self.control: PlayerControl = control
        self.selected_item_id: int = selected_item_id
        self.position: Vec2 = position
        self.velocity: Vec2 = velocity
        self.mount_type: int = mount_type
        self.potion_of_return_original_use_position: Vec2 = potion_of_return_original_use_position
        self.potion_of_return_home_position: Vec2 = potion_of_return_home_position
        self.net_camera_target: Vec2 = net_camera_target


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
