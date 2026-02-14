from typing import Optional, Tuple
from terrex.packets.base import SyncPacket
from terrex.structures.id import MessageID
from terrex.util.streamer import Reader, Writer
from terrex.structures.vec2 import Vec2

# Константы для флагов PulleyMode
PULLEY_HAS_VEL = 0x04

# Константы для флагов PlayerAction
PLAYER_ACTION_HAS_ORIG_AND_HOME_POS = 0x40

class PlayerControls(SyncPacket):
    id = MessageID.PlayerControls

    def __init__(
        self,
        player_id: int = 0,
        keys: int = 0,
        pulley: int = 0,
        action: int = 0,
        sleep_info: int = 0,
        selected_item: int = 0,
        pos: Vec2 = None,
        vel: Optional[Vec2] = None,
        original_and_home_pos: Optional[Tuple[Vec2, Vec2]] = None,
    ):
        self.player_id = player_id
        self.keys = keys
        self.pulley = pulley
        self.action = action
        self.sleep_info = sleep_info
        self.selected_item = selected_item
        self.pos = pos or Vec2(0.0, 0.0)
        self.vel = vel
        self.original_and_home_pos = original_and_home_pos

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()
        self.keys = reader.read_byte()
        self.pulley = reader.read_byte()
        self.action = reader.read_byte()
        self.sleep_info = reader.read_byte()
        self.selected_item = reader.read_byte()
        self.pos = Vec2.read(reader)

        self.vel = None
        if self.pulley & PULLEY_HAS_VEL:
            self.vel = Vec2.read(reader)

        self.original_and_home_pos = None
        if self.action & PLAYER_ACTION_HAS_ORIG_AND_HOME_POS:
            orig_pos = Vec2.read(reader)
            home_pos = Vec2.read(reader)
            self.original_and_home_pos = (orig_pos, home_pos)

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)
        writer.write_byte(self.keys)

        pulley_flags = self.pulley
        if self.vel is not None:
            pulley_flags |= PULLEY_HAS_VEL
        writer.write_byte(pulley_flags)

        action_flags = self.action
        if self.original_and_home_pos is not None:
            action_flags |= PLAYER_ACTION_HAS_ORIG_AND_HOME_POS
        writer.write_byte(action_flags)

        writer.write_byte(self.sleep_info)
        writer.write_byte(self.selected_item)
        self.pos.write(writer)

        if self.vel is not None:
            self.vel.write(writer)

        if self.original_and_home_pos is not None:
            self.original_and_home_pos[0].write(writer)
            self.original_and_home_pos[1].write(writer)

