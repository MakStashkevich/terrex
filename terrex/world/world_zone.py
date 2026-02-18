from terrex.structures.bits_byte import BitsByte


class WorldZone:
    def __init__(
        self,
        zone1: BitsByte | None = None,
        zone2: BitsByte | None = None,
        zone3: BitsByte | None = None,
        zone4: BitsByte | None = None,
        zone5: BitsByte | None = None,
    ):
        self.zone1 = zone1 or BitsByte()
        self.zone2 = zone2 or BitsByte()
        self.zone3 = zone3 or BitsByte()
        self.zone4 = zone4 or BitsByte()
        self.zone5 = zone5 or BitsByte()

    def update(
        self,
        zone1: BitsByte | None = None,
        zone2: BitsByte | None = None,
        zone3: BitsByte | None = None,
        zone4: BitsByte | None = None,
        zone5: BitsByte | None = None,
    ) -> None:
        if zone1:
            self.zone1 = zone1
        if zone2:
            self.zone2 = zone2
        if zone3:
            self.zone3 = zone3
        if zone4:
            self.zone4 = zone4
        if zone5:
            self.zone5 = zone5

    # zone1
    @property
    def dungeon(self):
        return self.zone1[0]

    @dungeon.setter
    def dungeon(self, val):
        self.zone1[0] = val

    @property
    def corrupt(self):
        return self.zone1[1]

    @corrupt.setter
    def corrupt(self, val):
        self.zone1[1] = val

    @property
    def hallow(self):
        return self.zone1[2]

    @hallow.setter
    def hallow(self, val):
        self.zone1[2] = val

    @property
    def meteor(self):
        return self.zone1[3]

    @meteor.setter
    def meteor(self, val):
        self.zone1[3] = val

    @property
    def jungle(self):
        return self.zone1[4]

    @jungle.setter
    def jungle(self, val):
        self.zone1[4] = val

    @property
    def snow(self):
        return self.zone1[5]

    @snow.setter
    def snow(self, val):
        self.zone1[5] = val

    @property
    def crimson(self):
        return self.zone1[6]

    @crimson.setter
    def crimson(self, val):
        self.zone1[6] = val

    @property
    def water_candle(self):
        return self.zone1[7]

    @water_candle.setter
    def water_candle(self, val):
        self.zone1[7] = val

    # zone2
    @property
    def peace_candle(self):
        return self.zone2[0]

    @peace_candle.setter
    def peace_candle(self, val):
        self.zone2[0] = val

    @property
    def tower_solar(self):
        return self.zone2[1]

    @tower_solar.setter
    def tower_solar(self, val):
        self.zone2[1] = val

    @property
    def tower_vortex(self):
        return self.zone2[2]

    @tower_vortex.setter
    def tower_vortex(self, val):
        self.zone2[2] = val

    @property
    def tower_nebula(self):
        return self.zone2[3]

    @tower_nebula.setter
    def tower_nebula(self, val):
        self.zone2[3] = val

    @property
    def tower_stardust(self):
        return self.zone2[4]

    @tower_stardust.setter
    def tower_stardust(self, val):
        self.zone2[4] = val

    @property
    def desert(self):
        return self.zone2[5]

    @desert.setter
    def desert(self, val):
        self.zone2[5] = val

    @property
    def glowshroom(self):
        return self.zone2[6]

    @glowshroom.setter
    def glowshroom(self, val):
        self.zone2[6] = val

    @property
    def underground_desert(self):
        return self.zone2[7]

    @underground_desert.setter
    def underground_desert(self, val):
        self.zone2[7] = val

    # zone3
    @property
    def sky_height(self):
        return self.zone3[0]

    @sky_height.setter
    def sky_height(self, val):
        self.zone3[0] = val

    @property
    def overworld_height(self):
        return self.zone3[1]

    @overworld_height.setter
    def overworld_height(self, val):
        self.zone3[1] = val

    @property
    def dirt_layer_height(self):
        return self.zone3[2]

    @dirt_layer_height.setter
    def dirt_layer_height(self, val):
        self.zone3[2] = val

    @property
    def rock_layer_height(self):
        return self.zone3[3]

    @rock_layer_height.setter
    def rock_layer_height(self, val):
        self.zone3[3] = val

    @property
    def underworld_height(self):
        return self.zone3[4]

    @underworld_height.setter
    def underworld_height(self, val):
        self.zone3[4] = val

    @property
    def beach(self):
        return self.zone3[5]

    @beach.setter
    def beach(self, val):
        self.zone3[5] = val

    @property
    def rain(self):
        return self.zone3[6]

    @rain.setter
    def rain(self, val):
        self.zone3[6] = val

    @property
    def sandstorm(self):
        return self.zone3[7]

    @sandstorm.setter
    def sandstorm(self, val):
        self.zone3[7] = val

    # zone4
    @property
    def old_one_army(self):
        return self.zone4[0]

    @old_one_army.setter
    def old_one_army(self, val):
        self.zone4[0] = val

    @property
    def granite(self):
        return self.zone4[1]

    @granite.setter
    def granite(self, val):
        self.zone4[1] = val

    @property
    def marble(self):
        return self.zone4[2]

    @marble.setter
    def marble(self, val):
        self.zone4[2] = val

    @property
    def hive(self):
        return self.zone4[3]

    @hive.setter
    def hive(self, val):
        self.zone4[3] = val

    @property
    def gem_cave(self):
        return self.zone4[4]

    @gem_cave.setter
    def gem_cave(self, val):
        self.zone4[4] = val

    @property
    def lihzhard_temple(self):
        return self.zone4[5]

    @lihzhard_temple.setter
    def lihzhard_temple(self, val):
        self.zone4[5] = val

    @property
    def graveyard(self):
        return self.zone4[6]

    @graveyard.setter
    def graveyard(self, val):
        self.zone4[6] = val

    @property
    def shadow_candle(self):
        return self.zone4[7]

    @shadow_candle.setter
    def shadow_candle(self, val):
        self.zone4[7] = val

    # zone5
    @property
    def shimmer(self):
        return self.zone5[0]

    @shimmer.setter
    def shimmer(self, val):
        self.zone5[0] = val
