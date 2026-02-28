from terrex.net.bits_byte import BitsByte
from terrex.net.structure.vec2 import Vec2


class PlayerControl:
    def __init__(
        self,
        # keys
        up: bool = False,
        down: bool = False,
        left: bool = False,
        right: bool = False,
        jump: bool = False,
        use_item: bool = False,
        direction: int = 0,
        # pulley
        is_pulley: bool = False,
        pulley_dir: int = 0,
        velocity: Vec2 | None = None,
        vortex_stealth_active: bool = False,
        grav_dir: float = 0.0,
        shield_raised: bool = False,
        ghost: bool = False,
        mount_active: bool = False,
        # active
        try_keeping_hovering_up: bool = False,
        is_void_vault_enabled: bool = False,
        is_sitting: bool = False,
        downed_DD2_event_any_difficulty: bool = False,
        is_petting: bool = False,
        is_pet_small: bool = False,
        has_potion_of_return_original_use_position: bool = False,
        try_keeping_hovering_down: bool = False,
        # sleep
        is_sleeping: bool = False,
        auto_reuse_all_weapons: bool = False,
        down_hold: bool = False,
        is_operating_another_entity: bool = False,
        use_tile: bool = False,
        has_net_camera_target: bool = False,
        last_item_use_attempt_success: bool = False,
    ):
        self.keys = BitsByte()
        self.keys[0] = up
        self.keys[1] = down
        self.keys[2] = left
        self.keys[3] = right
        self.keys[4] = jump
        self.keys[5] = use_item
        self.keys[6] = direction == 1

        self.pulley = BitsByte()
        self.pulley[0] = is_pulley
        self.pulley[1] = is_pulley and pulley_dir == 2
        self.pulley[2] = (velocity or Vec2(0, 0)) == Vec2(0, 0)
        self.pulley[3] = vortex_stealth_active
        self.pulley[4] = grav_dir == 1.0
        self.pulley[5] = shield_raised
        self.pulley[6] = ghost
        self.pulley[7] = mount_active

        self.active = BitsByte()
        self.active[0] = try_keeping_hovering_up
        self.active[1] = is_void_vault_enabled
        self.active[2] = is_sitting
        self.active[3] = downed_DD2_event_any_difficulty
        self.active[4] = is_petting
        self.active[5] = is_pet_small
        self.active[6] = has_potion_of_return_original_use_position
        self.active[7] = try_keeping_hovering_down

        self.sleep = BitsByte()
        self.sleep[0] = is_sleeping
        self.sleep[1] = auto_reuse_all_weapons
        self.sleep[2] = down_hold
        self.sleep[3] = is_operating_another_entity
        self.sleep[4] = use_tile
        self.sleep[5] = has_net_camera_target
        self.sleep[6] = last_item_use_attempt_success

    # keys
    @property
    def up(self):
        return self.keys[0]

    @up.setter
    def up(self, val: bool = False):
        self.keys[0] = val

    @property
    def down(self):
        return self.keys[1]

    @down.setter
    def down(self, val: bool = False):
        self.keys[1] = val

    @property
    def left(self):
        return self.keys[2]

    @left.setter
    def left(self, val: bool = False):
        self.keys[2] = val

    @property
    def right(self):
        return self.keys[3]

    @right.setter
    def right(self, val: bool = False):
        self.keys[3] = val

    @property
    def jump(self):
        return self.keys[4]

    @jump.setter
    def jump(self, val: bool = False):
        self.keys[4] = val

    @property
    def use_item(self):
        return self.keys[5]

    @use_item.setter
    def use_item(self, val: bool = False):
        self.keys[5] = val

    @property
    def right_direction(self):
        return self.keys[6]

    @right_direction.setter
    def right_direction(self, val: bool = False):
        self.keys[6] = val

    # pulley
    @property
    def is_pulley(self):
        return self.pulley[0]

    @is_pulley.setter
    def is_pulley(self, val: bool = False):
        self.pulley[0] = val

    @property
    def pulley_up(self):
        return self.pulley[1]

    @pulley_up.setter
    def pulley_up(self, val: bool = False):
        self.pulley[1] = val

    @property
    def has_velocity(self):
        return self.pulley[2]

    @has_velocity.setter
    def has_velocity(self, val: bool = False):
        self.pulley[2] = val

    @property
    def vortex_stealth_active(self):
        return self.pulley[3]

    @vortex_stealth_active.setter
    def vortex_stealth_active(self, val: bool = False):
        self.pulley[3] = val

    @property
    def inverted_gravity(self):
        return self.pulley[4]

    @inverted_gravity.setter
    def inverted_gravity(self, val: bool = False):
        self.pulley[4] = val

    @property
    def shield_raised(self):
        return self.pulley[5]

    @shield_raised.setter
    def shield_raised(self, val: bool = False):
        self.pulley[5] = val

    @property
    def ghost(self):
        return self.pulley[6]

    @ghost.setter
    def ghost(self, val: bool = False):
        self.pulley[6] = val

    @property
    def mount_active(self):
        return self.pulley[7]

    @mount_active.setter
    def mount_active(self, val: bool = False):
        self.pulley[7] = val

    # active
    @property
    def try_keeping_hovering_up(self):
        return self.active[0]

    @try_keeping_hovering_up.setter
    def try_keeping_hovering_up(self, val: bool = False):
        self.active[0] = val

    @property
    def is_void_vault_enabled(self):
        return self.active[1]

    @is_void_vault_enabled.setter
    def is_void_vault_enabled(self, val: bool = False):
        self.active[1] = val

    @property
    def is_sitting(self):
        return self.active[2]

    @is_sitting.setter
    def is_sitting(self, val: bool = False):
        self.active[2] = val

    @property
    def downed_DD2_event_any_difficulty(self):
        return self.active[3]

    @downed_DD2_event_any_difficulty.setter
    def downed_DD2_event_any_difficulty(self, val: bool = False):
        self.active[3] = val

    @property
    def is_petting(self):
        return self.active[4]

    @is_petting.setter
    def is_petting(self, val: bool = False):
        self.active[4] = val

    @property
    def is_pet_small(self):
        return self.active[5]

    @is_pet_small.setter
    def is_pet_small(self, val: bool = False):
        self.active[5] = val

    @property
    def has_potion_of_return_original_use_position(self):
        return self.active[6]

    @has_potion_of_return_original_use_position.setter
    def has_potion_of_return_original_use_position(self, val: bool = False):
        self.active[6] = val

    @property
    def try_keeping_hovering_down(self):
        return self.active[7]

    @try_keeping_hovering_down.setter
    def try_keeping_hovering_down(self, val: bool = False):
        self.active[7] = val

    # sleep
    @property
    def is_sleeping(self):
        return self.sleep[0]

    @is_sleeping.setter
    def is_sleeping(self, val: bool = False):
        self.sleep[0] = val

    @property
    def auto_reuse_all_weapons(self):
        return self.sleep[1]

    @auto_reuse_all_weapons.setter
    def auto_reuse_all_weapons(self, val: bool = False):
        self.sleep[1] = val

    @property
    def down_hold(self):
        return self.sleep[2]

    @down_hold.setter
    def down_hold(self, val: bool = False):
        self.sleep[2] = val

    @property
    def is_operating_another_entity(self):
        return self.sleep[3]

    @is_operating_another_entity.setter
    def is_operating_another_entity(self, val: bool = False):
        self.sleep[3] = val

    @property
    def use_tile(self):
        return self.sleep[4]

    @use_tile.setter
    def use_tile(self, val: bool = False):
        self.sleep[4] = val

    @property
    def has_net_camera_target(self):
        return self.sleep[5]

    @has_net_camera_target.setter
    def has_net_camera_target(self, val: bool = False):
        self.sleep[5] = val

    @property
    def last_item_use_attempt_success(self):
        return self.sleep[6]

    @last_item_use_attempt_success.setter
    def last_item_use_attempt_success(self, val: bool = False):
        self.sleep[6] = val
