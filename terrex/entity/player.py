from terrex.entity.entity import Entity
from terrex.entity.npc import NPC
from terrex.structures.rgb import Rgb
from terrex.structures.variable.bool_var import BoolVar
from terrex.structures.variable.const_var import ConstVar
from terrex.structures.variable.float_var import FloatVar
from terrex.structures.variable.int_var import IntVar
from terrex.structures.variable.str_var import StrVar
from terrex.world.shape.base import RectangleArea
from terrex.world.shape.rectangle import Rectangle


class Player(Entity):
    name: str = StrVar("", max_len=20)

    # const
    DEFAULT_WIDTH: int = ConstVar(20)
    DEFAULT_HEIGHT: int = ConstVar(42)

    # size
    width: int = IntVar(int(DEFAULT_WIDTH))
    height: int = IntVar(int(DEFAULT_HEIGHT))

    # frame
    body_frame: Rectangle = Rectangle()
    leg_frame: Rectangle = Rectangle()

    # connection flags
    initialized: bool = BoolVar(False)
    logged_in: bool = BoolVar(False)

    # inventory
    inventory: list = []

    # skin
    skin_variant: int = IntVar(0)
    voice_variant: int = IntVar(1)
    voice_pitch_offset: float = FloatVar(0.0)
    hair: int = IntVar(0)
    hair_dye: int = IntVar(255)
    accessory_visibility: int = IntVar(0)
    hide_misc: bool = BoolVar(False)

    # skin colors
    hair_color: Rgb = Rgb(255, 255, 255)
    skin_color: Rgb = Rgb(255, 255, 255)
    eye_color: Rgb = Rgb(255, 255, 255)
    shirt_color: Rgb = Rgb(255, 255, 255)
    under_shirt_color: Rgb = Rgb(255, 255, 255)
    pants_color: Rgb = Rgb(255, 255, 255)
    shoe_color: Rgb = Rgb(255, 255, 255)

    # difficulty flag
    difficulty: int = IntVar(1)

    # biome torch flags
    using_biome_torches: bool = BoolVar(False)
    happy_fun_torch_time: bool = BoolVar(False)
    unlocked_biome_torches: bool = BoolVar(False)
    unlocked_super_cart: bool = BoolVar(False)
    enabled_super_cart: bool = BoolVar(False)

    # consumables flags
    used_aegis_crystal: bool = BoolVar(False)
    used_aegis_fruit: bool = BoolVar(False)
    used_arcane_crystal: bool = BoolVar(False)
    used_galaxy_pearl: bool = BoolVar(False)
    used_gummy_worm: bool = BoolVar(False)
    used_ambrosia: bool = BoolVar(False)
    ate_artisan_bread: bool = BoolVar(False)

    # health
    maxHP: int = IntVar(100, min=0, max=500)
    currHP: int = IntVar(100, min=0, max=500)

    # mana
    maxMana: int = IntVar(20, min=0, max=200)
    currMana: int = IntVar(20, min=0, max=400)

    # luck factors
    ladybug_luck_time_left: int = IntVar(0)
    torch_luck: float = FloatVar(0.0)
    luck_potion: int = IntVar(0)
    has_garden_gnome_nearby: bool = BoolVar(False)
    broken_mirror_bad_luck: bool = BoolVar(False)
    equipment_based_luck_bonus: float = FloatVar(0.0)
    coin_luck: float = FloatVar(0.0)
    kite_luck_level: int = IntVar(0)

    # effects
    stinky: bool = BoolVar(False)

    def __init__(self, name: str = "terrex"):
        self.name = name

        # frame
        self.body_frame.width = 40
        self.body_frame.height = 56
        self.leg_frame.width = 40
        self.leg_frame.height = 56

        # todo: create inventory logic
        self.inventory = []
        for i in range(0, 72):
            self.inventory.append("Dummy Item")

    # ------------------------------
    # Player Luck Calculation
    # ------------------------------

    def get_ladybug_luck(self) -> float:
        """Calculates ladybug luck contribution (-1..1)."""
        if self.ladybug_luck_time_left > 0:
            return self.ladybug_luck_time_left / NPC.lady_bug_good_luck_time
        elif self.ladybug_luck_time_left < 0:
            return -self.ladybug_luck_time_left / NPC.lady_bug_bad_luck_time
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
        luck = 0.0
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
