import time

from terrex.event.types import PlayerControlUpdateEvent
from terrex.id import MessageID
from terrex.net.player_control import PlayerControl
from terrex.net.streamer import Reader, Writer
from terrex.net.bits_byte import BitsByte
from terrex.net.structure.vec2 import Vec2
from terrex.packet.base import SyncPacket


class PlayerControls(SyncPacket):
    id = MessageID.PlayerControls

    def __init__(
        self,
        player_id: int = -1,
        control: PlayerControl | None = None,
        selected_item_id: int = 0,
        position: Vec2 | None = None,
        velocity: Vec2 | None = None,
        mount_type: int = 0,
        potion_of_return_original_use_position: Vec2 | None = None,
        potion_of_return_home_position: Vec2 | None = None,
        net_camera_target: Vec2 | None = None,
    ):
        self.player_id = player_id
        self.control = control or PlayerControl()

        self.selected_item_id = selected_item_id
        self.position = position or Vec2()

        self.velocity = velocity or Vec2()
        self.control.has_velocity = self.velocity != Vec2(0, 0)

        self.mount_type = mount_type
        self.control.mount_active = self.mount_type > 0

        self.potion_of_return_original_use_position = (
            potion_of_return_original_use_position or Vec2()
        )
        self.potion_of_return_home_position = potion_of_return_home_position or Vec2()
        self.control.has_potion_of_return_original_use_position = (
            self.potion_of_return_original_use_position != Vec2(0, 0)
        )

        self.net_camera_target = net_camera_target or Vec2()
        self.control.has_net_camera_target = self.net_camera_target != Vec2(0, 0)

    def read(self, reader: Reader) -> None:
        self.player_id = reader.read_byte()

        self.control = PlayerControl()
        self.control.keys = BitsByte(reader.read_byte())
        self.control.pulley = BitsByte(reader.read_byte())
        self.control.active = BitsByte(reader.read_byte())
        self.control.sleep = BitsByte(reader.read_byte())

        self.selected_item_id = reader.read_byte()
        self.position = Vec2.read(reader)

        self.velocity = Vec2()
        if self.control.has_velocity:
            self.velocity = Vec2.read(reader)

        self.mount_type = 0
        if self.control.mount_active:
            self.mount_type = reader.read_ushort()

        self.potion_of_return_original_use_position = Vec2()
        self.potion_of_return_home_position = Vec2()
        if self.control.has_potion_of_return_original_use_position:
            self.potion_of_return_original_use_position = Vec2.read(reader)
            self.potion_of_return_home_position = Vec2.read(reader)

        self.net_camera_target = Vec2()
        if self.control.has_net_camera_target:
            self.net_camera_target = Vec2.read(reader)

    async def handle(self, world, player, evman):
        if not self.player_id in world.players:
            # print(f'player_id={self.player_id} moved to position={self.position} with velocity={self.velocity} left={self.control.left}, right={self.control.right}, up={self.control.up}, down={self.control.down}, jump={self.control.jump} time={time.time()}')
            return

        current_player = world.players[self.player_id]
        current_player.position = self.position
        current_player.velocity = self.velocity
        current_player.control = self.control
        # todo: update player mount, item and other

        evman.raise_event(
            PlayerControlUpdateEvent(
                self,
                self.player_id,
                self.control,
                self.selected_item_id,
                self.position,
                self.velocity,
                self.mount_type,
                self.potion_of_return_original_use_position,
                self.potion_of_return_home_position,
                self.net_camera_target,
            )
        )

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.player_id)

        writer.write_byte(int(self.control.keys))
        writer.write_byte(int(self.control.pulley))
        writer.write_byte(int(self.control.active))
        writer.write_byte(int(self.control.sleep))

        writer.write_byte(self.selected_item_id)
        self.position.write(writer)

        if self.control.has_velocity:
            self.velocity.write(writer)

        if self.control.mount_active:
            writer.write_ushort(self.mount_type)

        if self.control.has_potion_of_return_original_use_position:
            self.potion_of_return_original_use_position.write(writer)
            self.potion_of_return_home_position.write(writer)

        if self.control.has_net_camera_target:
            self.net_camera_target.write(writer)
