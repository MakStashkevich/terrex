from terrex.packet.base import SyncPacket
from terrex.id import MessageID
from terrex.net.structure.rgb import Rgb
from terrex.net.streamer import Reader, Writer


class SyncPlayer(SyncPacket):
    id = MessageID.SyncPlayer

    def __init__(
        self,
        player_id: int = 0,
        skin_variant: int = 0,
        voice_variant: int = 0,
        voice_pitch_offset: float = 0.0,
        hair: int = 0,
        name: str = "",
        hair_dye: int = 255,
        accessory_visibility: int = 0,
        hide_misc: bool = False,
        hair_color: Rgb | None = None,
        skin_color: Rgb | None = None,
        eye_color: Rgb | None = None,
        shirt_color: Rgb | None = None,
        under_shirt_color: Rgb | None = None,
        pants_color: Rgb | None = None,
        shoe_color: Rgb | None = None,
        difficulty_flags: int = 0,
        biome_torch_flags: int = 0,
        consumables_flags: int = 0,
    ):
        self.player_id = player_id
        self.skin_variant = skin_variant
        self.voice_variant = voice_variant
        self.voice_pitch_offset = voice_pitch_offset
        self.hair = hair
        self.name = name
        self.hair_dye = hair_dye
        self.accessory_visibility = accessory_visibility
        self.hide_misc = hide_misc
        self.hair_color = hair_color or Rgb(255, 255, 255)
        self.skin_color = skin_color or Rgb(255, 255, 255)
        self.eye_color = eye_color or Rgb(255, 255, 255)
        self.shirt_color = shirt_color or Rgb(255, 255, 255)
        self.under_shirt_color = under_shirt_color or Rgb(255, 255, 255)
        self.pants_color = pants_color or Rgb(255, 255, 255)
        self.shoe_color = shoe_color or Rgb(255, 255, 255)
        self.difficulty_flags = difficulty_flags
        self.biome_torch_flags = biome_torch_flags
        self.consumables_flags = consumables_flags

    def read(self, reader: Reader):
        self.player_id = reader.read_byte()
        self.skin_variant = reader.read_byte()
        self.voice_variant = reader.read_byte()
        self.voice_pitch_offset = reader.read_float()
        self.hair = reader.read_byte()
        self.name = reader.read_dotnet_string()
        self.hair_dye = reader.read_byte()
        self.accessory_visibility = reader.read_ushort()
        self.hide_misc = reader.read_bool()
        self.hair_color = Rgb.read(reader)
        self.skin_color = Rgb.read(reader)
        self.eye_color = Rgb.read(reader)
        self.shirt_color = Rgb.read(reader)
        self.under_shirt_color = Rgb.read(reader)
        self.pants_color = Rgb.read(reader)
        self.shoe_color = Rgb.read(reader)
        self.difficulty_flags = reader.read_byte()
        self.biome_torch_flags = reader.read_byte()
        self.consumables_flags = reader.read_byte()

    def write(self, writer: Writer):
        writer.write_byte(self.player_id)
        writer.write_byte(self.skin_variant)
        writer.write_byte(self.voice_variant)
        writer.write_float(self.voice_pitch_offset)
        writer.write_byte(self.hair)
        writer.write_dotnet_string(self.name)
        writer.write_byte(self.hair_dye)
        writer.write_ushort(self.accessory_visibility)
        writer.write_bool(self.hide_misc)
        self.hair_color.write(writer)
        self.skin_color.write(writer)
        self.eye_color.write(writer)
        self.shirt_color.write(writer)
        self.under_shirt_color.write(writer)
        self.pants_color.write(writer)
        self.shoe_color.write(writer)
        writer.write_byte(self.difficulty_flags)
        writer.write_byte(self.biome_torch_flags)
        writer.write_byte(self.consumables_flags)

    def get_hide_visible_accessory(self, index: int) -> bool:
        """Get if accessory at index is hidden (bit index in accessory_visibility)."""
        return bool((self.accessory_visibility & (1 << index)) != 0)

    def set_hide_visible_accessory(self, index: int, hide: bool):
        """Set if accessory at index is hidden."""
        mask = 1 << index
        if hide:
            self.accessory_visibility |= mask
        else:
            self.accessory_visibility &= ~mask

    def set_difficulty(self, difficulty: int):
        """Set player difficulty: 0-journey, 1-classic, 2-mediumcore, 3-hardcore."""
        self.difficulty_flags &= ~(1 | (1 << 1) | (1 << 3))  # clear difficulty bits
        if difficulty == 1:
            self.difficulty_flags |= 1 << 0
        elif difficulty == 2:
            self.difficulty_flags |= 1 << 1
        elif difficulty == 3:
            self.difficulty_flags |= 1 << 3

    def get_difficulty(self) -> int:
        """Get player difficulty."""
        if self.difficulty_flags & 1:
            return 1
        if self.difficulty_flags & (1 << 1):
            return 2
        if self.difficulty_flags & (1 << 3):
            return 3
        return 0

    @property
    def extra_accessory(self) -> bool:
        return bool(self.difficulty_flags & (1 << 2))

    @extra_accessory.setter
    def extra_accessory(self, value: bool):
        mask = 1 << 2
        if value:
            self.difficulty_flags |= mask
        else:
            self.difficulty_flags &= ~mask

    @property
    def using_biome_torches(self) -> bool:
        return bool(self.biome_torch_flags & 1)

    @using_biome_torches.setter
    def using_biome_torches(self, value: bool):
        mask = 1
        if value:
            self.biome_torch_flags |= mask
        else:
            self.biome_torch_flags &= ~mask

    @property
    def happy_fun_torch_time(self) -> bool:
        return bool(self.biome_torch_flags & (1 << 1))

    @happy_fun_torch_time.setter
    def happy_fun_torch_time(self, value: bool):
        mask = 1 << 1
        if value:
            self.biome_torch_flags |= mask
        else:
            self.biome_torch_flags &= ~mask

    @property
    def unlocked_biome_torches(self) -> bool:
        return bool(self.biome_torch_flags & (1 << 2))

    @unlocked_biome_torches.setter
    def unlocked_biome_torches(self, value: bool):
        mask = 1 << 2
        if value:
            self.biome_torch_flags |= mask
        else:
            self.biome_torch_flags &= ~mask

    @property
    def unlocked_super_cart(self) -> bool:
        return bool(self.biome_torch_flags & (1 << 3))

    @unlocked_super_cart.setter
    def unlocked_super_cart(self, value: bool):
        mask = 1 << 3
        if value:
            self.biome_torch_flags |= mask
        else:
            self.biome_torch_flags &= ~mask

    @property
    def enabled_super_cart(self) -> bool:
        return bool(self.biome_torch_flags & (1 << 4))

    @enabled_super_cart.setter
    def enabled_super_cart(self, value: bool):
        mask = 1 << 4
        if value:
            self.biome_torch_flags |= mask
        else:
            self.biome_torch_flags &= ~mask

    @property
    def used_aegis_crystal(self) -> bool:
        return bool(self.consumables_flags & 1)

    @used_aegis_crystal.setter
    def used_aegis_crystal(self, value: bool):
        mask = 1
        if value:
            self.consumables_flags |= mask
        else:
            self.consumables_flags &= ~mask

    @property
    def used_aegis_fruit(self) -> bool:
        return bool(self.consumables_flags & (1 << 1))

    @used_aegis_fruit.setter
    def used_aegis_fruit(self, value: bool):
        mask = 1 << 1
        if value:
            self.consumables_flags |= mask
        else:
            self.consumables_flags &= ~mask

    @property
    def used_arcane_crystal(self) -> bool:
        return bool(self.consumables_flags & (1 << 2))

    @used_arcane_crystal.setter
    def used_arcane_crystal(self, value: bool):
        mask = 1 << 2
        if value:
            self.consumables_flags |= mask
        else:
            self.consumables_flags &= ~mask

    @property
    def used_galaxy_pearl(self) -> bool:
        return bool(self.consumables_flags & (1 << 3))

    @used_galaxy_pearl.setter
    def used_galaxy_pearl(self, value: bool):
        mask = 1 << 3
        if value:
            self.consumables_flags |= mask
        else:
            self.consumables_flags &= ~mask

    @property
    def used_gummy_worm(self) -> bool:
        return bool(self.consumables_flags & (1 << 4))

    @used_gummy_worm.setter
    def used_gummy_worm(self, value: bool):
        mask = 1 << 4
        if value:
            self.consumables_flags |= mask
        else:
            self.consumables_flags &= ~mask

    @property
    def used_ambrosia(self) -> bool:
        return bool(self.consumables_flags & (1 << 5))

    @used_ambrosia.setter
    def used_ambrosia(self, value: bool):
        mask = 1 << 5
        if value:
            self.consumables_flags |= mask
        else:
            self.consumables_flags &= ~mask

    @property
    def ate_artisan_bread(self) -> bool:
        return bool(self.consumables_flags & (1 << 6))

    @ate_artisan_bread.setter
    def ate_artisan_bread(self, value: bool):
        mask = 1 << 6
        if value:
            self.consumables_flags |= mask
        else:
            self.consumables_flags &= ~mask
