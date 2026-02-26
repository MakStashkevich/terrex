from terrex.entity.entity import Entity
from terrex.entity.npc import NPC
from terrex.net.structure.rgb import Rgb
from terrex.net.variable.bool_var import BoolVar
from terrex.net.variable.const_var import ConstVar
from terrex.net.variable.float_var import FloatVar
from terrex.net.variable.int_var import IntVar
from terrex.net.variable.str_var import StrVar
from terrex.net.world_zone import WorldZone
from terrex.world.shape.rectangle import Rectangle


class Player(Entity):
    name: StrVar = StrVar("", max_len=20)

    # const
    DEFAULT_WIDTH: ConstVar = ConstVar(20)
    DEFAULT_HEIGHT: ConstVar = ConstVar(42)

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
    zone: WorldZone = WorldZone()

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

    def __init__(self, name: str = "terrex"):
        self.name = name

        # frame
        self.body_frame.width = 40
        self.body_frame.height = 56
        self.leg_frame.width = 40
        self.leg_frame.height = 56

        # todo: create inventory logic
        self.inventory = []
        for _ in range(0, 72):
            self.inventory.append("Dummy Item")

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
