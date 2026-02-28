from terrex.entity.entity import Entity
from terrex.entity.npc import NPC
from terrex.net.player_control import PlayerControl
from terrex.net.structure.rgb import Rgb
from terrex.net.structure.vec2 import Vec2
from terrex.net.tile_npc_data import TileNPCData
from terrex.net.variable.bool_var import BoolVar
from terrex.net.variable.const_var import ConstVar
from terrex.net.variable.float_var import FloatVar
from terrex.net.variable.int_var import IntVar
from terrex.net.variable.str_var import StrVar
from terrex.net.world_zone import WorldZone
from terrex.world.shape.rectangle import Rectangle
from terrex.world.world import World

tile_data = TileNPCData()


class Player(Entity):
    name: StrVar = StrVar("terrex", max_len=20)
    _target_position: Vec2 | None = None

    # const
    DEFAULT_WIDTH: ConstVar = ConstVar(20)
    DEFAULT_HEIGHT: ConstVar = ConstVar(42)

    TILE_SIZE: float = 16.0
    PLAYER_WIDTH: float = 20.0
    PLAYER_HEIGHT: float = 42.0
    GRAVITY: float = 0.4
    MAX_FALL_SPEED: float = 10.0
    JUMP_SPEED: float = 5.01
    RUN_ACCELERATION: float = 0.08
    RUN_SLOWDOWN: float = 0.2
    MAX_RUN_SPEED: float = 3.0
    JUMP_HEIGHT_TILES: float = 15.0

    # size
    width: IntVar = IntVar(int(DEFAULT_WIDTH))
    height: IntVar = IntVar(int(DEFAULT_HEIGHT))

    # frame
    body_frame: Rectangle = Rectangle()
    leg_frame: Rectangle = Rectangle()

    # connection flags
    initialized: BoolVar = BoolVar(False)
    logged_in: BoolVar = BoolVar(False)

    # inventory
    inventory: list = []

    # world
    world: World
    chest_id: int = -1
    zone: WorldZone = WorldZone()
    npc_talk_id: int = -1

    # ???
    loadout_index: int = -1

    # controls
    control: PlayerControl = PlayerControl()
    position: Vec2 = Vec2(0, 0)
    velocity: Vec2 = Vec2(0, 0)
    gravity: float = 0.4  # default
    jump_height: int = 0

    # skin
    skin_variant: IntVar = IntVar(0)
    voice_variant: IntVar = IntVar(1)
    voice_pitch_offset: FloatVar = FloatVar(0.0)
    hair: IntVar = IntVar(0, min=0, max=228)
    hair_dye: IntVar = IntVar(255, min=0, max=255)
    accessory_visibility: IntVar = IntVar(0)
    hide_misc: BoolVar = BoolVar(False)

    # skin colors
    hair_color: Rgb = Rgb(151, 100, 69)
    skin_color: Rgb = Rgb(255, 125, 90)
    eye_color: Rgb = Rgb(105, 90, 75)
    shirt_color: Rgb = Rgb(175, 165, 140)
    under_shirt_color: Rgb = Rgb(160, 180, 215)
    pants_color: Rgb = Rgb(255, 230, 175)
    shoe_color: Rgb = Rgb(160, 105, 60)

    # difficulty flag
    difficulty: IntVar = IntVar(1)

    # pvp
    pvp_enabled: bool = False

    # team
    team: int = 0

    # buffs
    buffs: list[int] = []

    # biome torch flags
    using_biome_torches: BoolVar = BoolVar(False)
    happy_fun_torch_time: BoolVar = BoolVar(False)
    unlocked_biome_torches: BoolVar = BoolVar(False)
    unlocked_super_cart: BoolVar = BoolVar(False)
    enabled_super_cart: BoolVar = BoolVar(False)

    # consumables flags
    used_aegis_crystal: BoolVar = BoolVar(False)
    used_aegis_fruit: BoolVar = BoolVar(False)
    used_arcane_crystal: BoolVar = BoolVar(False)
    used_galaxy_pearl: BoolVar = BoolVar(False)
    used_gummy_worm: BoolVar = BoolVar(False)
    used_ambrosia: BoolVar = BoolVar(False)
    ate_artisan_bread: BoolVar = BoolVar(False)

    # health
    maxHP: IntVar = IntVar(100, min=0, max=500)
    currHP: IntVar = IntVar(100, min=0, max=500)

    # mana
    maxMana: IntVar = IntVar(20, min=0, max=200)
    currMana: IntVar = IntVar(20, min=0, max=400)

    # luck factors
    ladybug_luck_time_left: IntVar = IntVar(0)
    torch_luck: FloatVar = FloatVar(0.0)
    luck_potion: IntVar = IntVar(0)
    has_garden_gnome_nearby: BoolVar = BoolVar(False)
    broken_mirror_bad_luck: BoolVar = BoolVar(False)
    equipment_based_luck_bonus: FloatVar = FloatVar(0.0)
    coin_luck: FloatVar = FloatVar(0.0)
    kite_luck_level: IntVar = IntVar(0)

    # effects
    stinky: BoolVar = BoolVar(False)

    def __init__(self, world: World):
        self.world = world

        # frame
        self.body_frame.width = 40
        self.body_frame.height = 56
        self.leg_frame.width = 40
        self.leg_frame.height = 56

        # todo: create inventory logic
        self.inventory = []
        for _ in range(0, 72):
            self.inventory.append("Dummy Item")

        self.MAX_JUMP_H = self.JUMP_HEIGHT_TILES * self.TILE_SIZE
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
        return tile_solid[ttype] if isinstance(tile_solid, list) else False

    def is_tile_solid_top(self, tx: int, ty: int) -> bool:
        ttype = self.get_tile_type(tx, ty)
        tile_solid_top = tile_data.tileSolidTop
        return tile_solid_top[ttype] if isinstance(tile_solid_top, list) else False

    def world_to_tile(self, x: float, y: float) -> tuple[int, int]:
        return int(x // self.TILE_SIZE), int(y // self.TILE_SIZE)

    def can_stand(self, pos: Vec2) -> bool:
        left = int(pos.x // self.TILE_SIZE)
        right = int((pos.x + self.PLAYER_WIDTH - 1) // self.TILE_SIZE)
        top = int(pos.y // self.TILE_SIZE)
        bottom = int((pos.y + self.PLAYER_HEIGHT - 1) // self.TILE_SIZE)
        max_ty = self.world.max_tiles_y
        max_tx = self.world.max_tiles_x
        if bottom >= max_ty or left < 0 or right >= max_tx or top < 0:
            return False
        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                if self.is_tile_solid_top(tx, ty):
                    if (
                        ty == bottom
                        and pos.y + self.PLAYER_HEIGHT > (ty + 1) * self.TILE_SIZE
                        and not self.control.down
                    ):
                        return False
                elif self.is_tile_solid(tx, ty):
                    return False
        return True

    def is_on_ground(self, pos: Vec2 = None) -> bool:
        if pos is None:
            pos = self.position
        below = pos.y + self.PLAYER_HEIGHT
        tile_ty = int(below // self.TILE_SIZE)
        left = int(pos.x // self.TILE_SIZE)
        right = int((pos.x + self.PLAYER_WIDTH - 1) // self.TILE_SIZE)
        max_ty = self.world.max_tiles_y
        if tile_ty >= max_ty:
            return False
        for tx in range(left, right + 1):
            if self.is_tile_solid(tx, tile_ty) or self.is_tile_solid_top(tx, tile_ty):
                return True
        return False

    def update(self, tick: int):
        if self._target_position is None or self.position == self._target_position:
            self.control.left = False
            self.control.right = False
            self.control.jump = False
            self.control.down = False
            return

        # Compute control based on target
        dx = self._target_position.x - self.position.x
        dy = self._target_position.y - self.position.y
        self.gravity_dir = 1.0 if dy >= 0 else -1.0
        self.control.left = dx < -self.TILE_SIZE / 2
        self.control.right = dx > self.TILE_SIZE / 2
        self.control.down = dy > 0 and self.is_on_ground()
        self.control.jump = dy < 0

        # Horizontal movement
        if self.control.left:
            if self.velocity.x > -self.MAX_RUN_SPEED:
                self.velocity.x -= self.RUN_ACCELERATION
        elif self.control.right:
            if self.velocity.x < self.MAX_RUN_SPEED:
                self.velocity.x += self.RUN_ACCELERATION
        else:
            if self.velocity.x > self.RUN_SLOWDOWN:
                self.velocity.x -= self.RUN_SLOWDOWN
            elif self.velocity.x < -self.RUN_SLOWDOWN:
                self.velocity.x += self.RUN_SLOWDOWN
            else:
                self.velocity.x = 0.0

        # Vertical movement
        # Set jump hold frames at takeoff (proportional)
        if self.control.jump and self.is_on_ground() and self.jump_hold_frames == 0:
            dy = self._target_position.y - self.position.y
            required_h_up = -dy if dy < 0 else 0.0
            scale = min(1.0, required_h_up / self.MAX_JUMP_H)
            self.jump_hold_frames = int(50 * scale)

        # Gravity
        self.velocity.y += self.GRAVITY * self.gravity_dir

        # Jump hold override (Terraria style)
        if self.jump_hold_frames > 0:
            if self.velocity.y == 0.0:
                self.jump_hold_frames = 0
            else:
                self.velocity.y = self.gravity_dir * self.JUMP_SPEED
                self.jump_hold_frames -= 1

        if self.velocity.y > self.MAX_FALL_SPEED:
            self.velocity.y = self.MAX_FALL_SPEED

        # Tentative new position (DT = 1 tick)
        new_pos = Vec2(self.position.x + self.velocity.x, self.position.y + self.velocity.y)

        # Resolve ground collision
        below = new_pos.y + self.PLAYER_HEIGHT
        tile_ty = int(below // self.TILE_SIZE)
        left_tx = int(new_pos.x // self.TILE_SIZE)
        right_tx = int((new_pos.x + self.PLAYER_WIDTH - 1) // self.TILE_SIZE)
        landed = False  # not used????
        max_ty = self.world.max_tiles_y
        if tile_ty < max_ty:
            for tx in range(left_tx, right_tx + 1):
                if self.is_tile_solid(tx, tile_ty) or (
                    self.is_tile_solid_top(tx, tile_ty) and not self.control.down
                ):
                    if below <= (tile_ty + 1) * self.TILE_SIZE:
                        new_pos.y = tile_ty * self.TILE_SIZE - self.PLAYER_HEIGHT
                        self.velocity.y = 0.0
                        landed = True
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
