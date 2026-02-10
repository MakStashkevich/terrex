from xml.dom.minidom import Entity
from terrex.data.npc import NPC
from terrex.structures.rgb import Rgb


class Player(Entity):
    name: str = ""

    # size
    width = 20
    height = 42

    # connection flags
    initialized: bool = False
    logged_in: bool = False

    # inventory
    inventory: list = []

    # skin
    skin_variant: int = 0
    voice_variant: int = 1
    voice_pitch_offset: float = 0.0
    hair: int = 0
    hair_dye: int = 255
    accessory_visibility: int = 0
    hide_misc: bool = False

    # skin colors
    hair_color: Rgb = Rgb(255, 255, 255)
    skin_color: Rgb = Rgb(255, 255, 255)
    eye_color: Rgb = Rgb(255, 255, 255)
    shirt_color: Rgb = Rgb(255, 255, 255)
    under_shirt_color: Rgb = Rgb(255, 255, 255)
    pants_color: Rgb = Rgb(255, 255, 255)
    shoe_color: Rgb = Rgb(255, 255, 255)

    # difficulty flag
    difficulty: int = 1

    # biome torch flags
    using_biome_torches: bool = True
    happy_fun_torch_time: bool = False
    unlocked_biome_torches: bool = True
    unlocked_super_cart: bool = False
    enabled_super_cart: bool = False

    # consumables flags
    used_aegis_crystal: bool = True
    used_aegis_fruit: bool = True
    used_arcane_crystal: bool = True
    used_galaxy_pearl: bool = True
    used_gummy_worm: bool = True
    used_ambrosia: bool = True
    ate_artisan_bread: bool = True

    # health
    maxHP: int = 400
    currHP: int = 400

    # mana
    maxMana: int = 50
    currMana: int = 10

    # luck factors
    ladybug_luck_time_left: int = 0
    torch_luck: float = 0.0
    luck_potion: int = 0
    has_garden_gnome_nearby: bool = False
    broken_mirror_bad_luck: bool = False
    equipment_based_luck_bonus: float = 0.0
    coin_luck: float = 0.0
    kite_luck_level: int = 0

    # effects
    stinky: bool = False

    def __init__(self, name: str = "terrex"):
        self.name = name  # max 20 chars

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
