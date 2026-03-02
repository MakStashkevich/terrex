from terrex.entity.entity import Entity
from terrex.entity.npc import NPC
from terrex.item.item import Item
from terrex.net.player_control import PlayerControl
from terrex.net.structure.rgb import Rgb
from terrex.net.structure.vec2 import Vec2
from terrex.net.tile_npc_data import TileNPCData
from terrex.net.world_zone import WorldZone
from terrex.world.shape.rectangle import Rectangle
from terrex.world.world import World

tile_data = TileNPCData()


DEFAULT_WIDTH: int = 20
DEFAULT_HEIGHT: int = 42

TILE_SIZE: float = 16.0
PLAYER_WIDTH: float = 20.0
PLAYER_HEIGHT: float = 42.0
GRAVITY: float = 0.4
MAX_FALL_SPEED: float = 10.0
JUMP_SPEED: float = 5.01
RUN_ACCELERATION: float = 0.08
RUN_SLOWDOWN: float = 0.2
MAX_RUN_SPEED: float = 3.0
JUMP_HEIGHT: float = 15.0


class Player(Entity):
    def __init__(self, _world: World):
        super().__init__()

        self.uuid = "01032c81-623f-4435-85e5-e0ec816b09ca"
        self.name: str = "terrex"
        self.target_position: Vec2 | None = None

        # size
        self.width: int = DEFAULT_WIDTH
        self.height: int = DEFAULT_HEIGHT

        # frame
        self.body_frame: Rectangle = Rectangle(width=40, height=56)
        self.leg_frame: Rectangle = Rectangle(width=40, height=56)
        # self.head_frame: Rectangle = Rectangle()
        # self.hair_frame: Rectangle = Rectangle()

        # connection flags
        self.initialized: bool = False
        self.logged_in: bool = False

        # inventory
        self.inventory: list[Item] = []
        # todo: create inventory logic
        for _ in range(0, 72):
            self.inventory.append(Item())

        # world
        self.world: World = _world
        self.chest_id: int = -1
        self.zone: WorldZone = WorldZone()
        self.npc_talk_id: int = -1

        # ???
        self.loadout_index: int = -1

        # controls
        self.control: PlayerControl = PlayerControl()

        # skin
        self.skin_variant: int = 0
        self.voice_variant: int = 1
        self.voice_pitch_offset: float = 0.0
        self.hair: int = 0
        self.hair_dye: int = 255
        self.accessory_visibility: int = 0
        self.hide_misc: bool = False

        # skin colors
        self.hair_color: Rgb = Rgb(151, 100, 69)
        self.skin_color: Rgb = Rgb(255, 125, 90)
        self.eye_color: Rgb = Rgb(105, 90, 75)
        self.shirt_color: Rgb = Rgb(175, 165, 140)
        self.under_shirt_color: Rgb = Rgb(160, 180, 215)
        self.pants_color: Rgb = Rgb(255, 230, 175)
        self.shoe_color: Rgb = Rgb(160, 105, 60)

        # difficulty flag
        self.difficulty: int = 1

        # pvp
        self.pvp_enabled: bool = False

        # team
        self.team: int = 0

        # buffs
        self.buffs: list[int] = []

        # biome torch flags
        self.using_biome_torches: bool = False
        self.happy_fun_torch_time: bool = False
        self.unlocked_biome_torches: bool = False
        self.unlocked_super_cart: bool = False
        self.enabled_super_cart: bool = False

        # consumables flags
        self.used_aegis_crystal: bool = False
        self.used_aegis_fruit: bool = False
        self.used_arcane_crystal: bool = False
        self.used_galaxy_pearl: bool = False
        self.used_gummy_worm: bool = False
        self.used_ambrosia: bool = False
        self.ate_artisan_bread: bool = False

        # health
        self.maxHP: int = 100
        self.currHP: int = 100

        # mana
        self.maxMana: int = 20
        self.currMana: int = 20

        # luck factors
        self.ladybug_luck_time_left: int = 0
        self.torch_luck: float = 0.0
        self.luck_potion: int = 0
        self.has_garden_gnome_nearby: bool = False
        self.broken_mirror_bad_luck: bool = False
        self.equipment_based_luck_bonus: float = 0.0
        self.coin_luck: float = 0.0
        self.kite_luck_level: int = 0

        # effects
        self.stinky: bool = False

        # --------------

        self.jump_hold_frames = 0
        self.gravity_dir = 1.0

    def get_tile_type(self, tx: int, ty: int) -> int:
        tile = self.world.tiles.get(tx, ty)
        return tile.type if tile else 0

    def is_tile_solid(self, tx: int, ty: int) -> bool:
        ttype = self.get_tile_type(tx, ty)
        if ttype == 0:
            return False
        if self.is_tile_solid_top(tx, ty):
            return False
        tile_solid = tile_data.tileSolid
        return tile_solid[ttype]

    def is_tile_solid_top(self, tx: int, ty: int) -> bool:
        ttype = self.get_tile_type(tx, ty)
        tile_solid_top = tile_data.tileSolidTop
        return tile_solid_top[ttype]

    def world_to_tile(self, x: float, y: float) -> tuple[int, int]:
        return int(x // TILE_SIZE), int(y // TILE_SIZE)

    def can_stand(self, pos: Vec2) -> bool:
        left = int(pos.x // TILE_SIZE)
        right = int((pos.x + self.width) // TILE_SIZE)
        top = int(pos.y // TILE_SIZE)
        bottom = int((pos.y + self.height) // TILE_SIZE)
        max_ty = self.world.max_tiles_y
        max_tx = self.world.max_tiles_x
        if bottom >= max_ty or left < 0 or right >= max_tx or top < 0:
            return False
        for ty in range(top, bottom):
            for tx in range(left, right):
                if self.is_tile_solid_top(tx, ty):
                    if (
                        ty == bottom
                        and pos.y + self.height > (ty + 1) * TILE_SIZE
                        and not self.control.down
                    ):
                        return False
                elif self.is_tile_solid(tx, ty):
                    return False
        return True

    def is_on_ground(self, pos: Vec2 | None = None) -> bool:
        if pos is None:
            pos = self.position
        below = pos.y + self.height + 1
        tile_ty = int(below // TILE_SIZE)
        left = int(pos.x // TILE_SIZE)
        right = int((pos.x + self.width) // TILE_SIZE)
        max_ty = self.world.max_tiles_y
        if tile_ty >= max_ty:
            return False
        for tx in range(left, right):
            if self.is_tile_solid(tx, tile_ty) or self.is_tile_solid_top(tx, tile_ty):
                return True
        return False

    def update(self, _: int):
        # https://github.com/tModLoader/tModLoader/wiki/Geometry
        if (
            self.target_position is None
            or self.position.distance_to(self.target_position) < TILE_SIZE
        ):
            self.control.left = False
            self.control.right = False
            self.control.jump = False
            self.control.down = False
            self.velocity = Vec2()
            return

        # Compute control based on target
        dx = self.target_position.x - self.position.x
        dy = self.target_position.y - self.position.y

        self.control.left = dx < -TILE_SIZE
        self.control.right = dx > TILE_SIZE

        is_horisontal_moving: bool = bool(self.control.left or self.control.right)
        is_on_ground: bool = self.is_on_ground()

        # print(f'self._target_position.y={self._target_position.y}, self.center.y={self.center.y}, dy={dy}, dy > 0={dy > 0}')
        if is_on_ground and dy < 0:
            px_left = int(self.position.x // TILE_SIZE)
            px_right = int((self.position.x + self.width) // TILE_SIZE)
            py_top = int((self.position.y) // TILE_SIZE)
            for ty_offset in range(0, 4):
                for tx_offset in range(-1, 3):
                    front_tx = px_left - tx_offset if self.control.left else px_right + tx_offset
                    above_ty = py_top - ty_offset
                    if (
                        front_tx > 0
                        and above_ty > 0
                        and (
                            self.is_tile_solid(front_tx, above_ty)
                            or self.is_tile_solid_top(front_tx, above_ty)
                        )
                    ):
                        self.control.jump = True
                        break
            self.control.down = False
        elif is_on_ground and dy > 0:
            self.control.jump = False
            self.control.down = True
        else:
            self.control.down = False
            self.control.jump = False

        # Horizontal movement
        if is_horisontal_moving and self.position.distance_to(self.target_position) > abs(
            self.velocity.x
        ):
            if self.control.left:
                if self.velocity.x > -MAX_RUN_SPEED:
                    self.velocity.x -= RUN_ACCELERATION
            elif self.control.right:
                if self.velocity.x < MAX_RUN_SPEED:
                    self.velocity.x += RUN_ACCELERATION
        else:
            if self.velocity.x > RUN_SLOWDOWN:
                self.velocity.x -= RUN_SLOWDOWN
            elif self.velocity.x < -RUN_SLOWDOWN:
                self.velocity.x += RUN_SLOWDOWN
            else:
                self.velocity.x = 0.0

        # Vertical movement
        # Set jump hold frames at takeoff (proportional)
        if self.control.jump and is_on_ground and self.jump_hold_frames == 0:
            dy = self.target_position.y - self.position.y
            required_h_up = -dy if dy < 0 else 0.0
            self.jump_hold_frames = int(required_h_up // JUMP_HEIGHT)

        # Gravity
        self.velocity.y += GRAVITY * self.gravity_dir

        # Jump hold override (Terraria style)
        if self.jump_hold_frames > 0:
            self.velocity.y = -self.gravity_dir * JUMP_SPEED
            self.jump_hold_frames -= 1

        if not self.control.jump and not is_on_ground:
            if self.gravity_dir == 1.0:
                if self.velocity.y > MAX_FALL_SPEED:
                    self.velocity.y = MAX_FALL_SPEED
            else:
                if self.velocity.y < -MAX_FALL_SPEED:
                    self.velocity.y = -MAX_FALL_SPEED

        # Tentative new position (DT = 1 tick)
        new_pos = Vec2(self.position.x + self.velocity.x, self.position.y + self.velocity.y)

        # Resolve ground collision only during fall (v.y >= 0)
        if self.velocity.y >= 0:
            below = new_pos.y + self.height
            tile_ty = int(below // TILE_SIZE)
            left_tx = int(new_pos.x // TILE_SIZE)
            right_tx = int((new_pos.x + self.width) // TILE_SIZE)
            max_ty = self.world.max_tiles_y
            if tile_ty < max_ty:
                for tx in range(left_tx, right_tx):
                    if self.is_tile_solid(tx, tile_ty) or (
                        self.is_tile_solid_top(tx, tile_ty) and not self.control.down
                    ):
                        if below <= (tile_ty + 1) * TILE_SIZE:
                            new_pos.y = tile_ty * TILE_SIZE - self.height
                            self.velocity.y = 0.0
                            break

        # Validate new position
        if not self.can_stand(new_pos):
            new_pos = self.position
            self.velocity.x *= 0.5  # dampen
            self.velocity.y = 0.0

        self.position = new_pos

    # ------------------------------
    # Player Luck Calculation
    # ------------------------------

    def get_ladybug_luck(self) -> float:
        """Calculates ladybug luck contribution (-1..1)."""
        if self.ladybug_luck_time_left > 0:
            return float(self.ladybug_luck_time_left) / NPC.lady_bug_good_luck_time
        elif self.ladybug_luck_time_left < 0:
            return -float(self.ladybug_luck_time_left) / NPC.lady_bug_bad_luck_time
        return 0.0

    def calculate_coin_luck(self) -> float:
        """Calculates stepwise coinLuck bonus."""
        cl = self.coin_luck
        if cl <= 0:
            return 0.0
        elif cl <= 0.249:
            return 0.025
        elif cl <= 2.49:
            return 0.05
        elif cl <= 24.9:
            return 0.075
        elif cl <= 249:
            return 0.1
        elif cl <= 2490:
            return 0.125
        elif cl <= 24900:
            return 0.15
        elif cl <= 249000:
            return 0.175
        else:
            return 0.2

    def calculate_total_luck(self) -> float:
        """Returns the total current luck of the player (-0.4..1.0)."""
        luck: float = 0.0
        luck += self.get_ladybug_luck() * 0.2
        luck += self.torch_luck * 0.2

        # assuming luck_potion is integer tier
        # 1 - 5 min potion
        # 2 - 10 min potion
        # 3 - 15 min potion
        luck += self.luck_potion * 0.1
        luck += self.kite_luck_level * 0.1 / 3

        if self.used_galaxy_pearl:
            luck += 0.03

        # if (LanternNight.LanternsUp)
        # {
        # 	this.luck += 0.3f;
        # }

        if self.has_garden_gnome_nearby:
            luck += 0.2

        if self.stinky:
            luck -= 0.25

        luck += self.equipment_based_luck_bonus
        luck += self.calculate_coin_luck()

        if self.broken_mirror_bad_luck:
            luck -= 0.25

        return luck

    # todo: Update (every tick), ResetEffects, UpdateBuffs
