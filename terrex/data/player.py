from terrex.structures.rgb import Rgb


class Player(object):

    def __init__(self, name):
        self.playerID = 0
        self.name = "Terrex"
        
        # connection flags
        self.initialized = False
        self.logged_in = False
        
        # todo: create inventory logic
        self.inventory = []
        for i in range(0, 72):
            self.inventory.append("Dummy Item")
        
        # skin
        self.skinVariant = 0
        self.voice_variant = 0
        self.voice_pitch_offset = 0.0
        self.hair = 0
        self.hair_dye = 255
        self.accessory_visibility = [False] * 4
        self.hide_misc = False
        
        # skin colors
        self.hair_color = Rgb(255, 255, 255)
        self.skin_color = Rgb(255, 255, 255)
        self.eye_color = Rgb(255, 255, 255)
        self.shirt_color = Rgb(255, 255, 255)
        self.under_shirt_color = Rgb(255, 255, 255)
        self.pants_color = Rgb(255, 255, 255)
        self.shoe_color = Rgb(255, 255, 255)
        
        # difficulty flag
        self.difficulty = 1
        
        # biome torch flags
        self.using_biome_torches = True
        self.happy_fun_torch_time = False
        self.unlocked_biome_torches = True
        self.unlocked_super_cart = False
        self.enabled_super_cart = False
        
        # consumables flags
        self.used_aegis_crystal = True
        self.used_aegis_fruit = True
        self.used_arcane_crystal = True
        self.used_galaxy_pearl = True
        self.used_gummy_worm = True
        self.used_ambrosia = True
        self.ate_artisan_bread = True

        # health
        self.maxHP = 400
        self.currHP = 400

        # mana
        self.maxMana = 50
        self.currMana = 10

        # todo: position
        self.x = -1
        self.y = -1
