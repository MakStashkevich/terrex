from .creative_power import CreativePower

from .difficulty_slider_power import DifficultySliderPower
from .far_placement_range_power import FarPlacementRangePower
from .freeze_rain_power import FreezeRainPower
from .freeze_time_power import FreezeTimePower
from .freeze_wind_direction_and_strength_power import (
    FreezeWindDirectionAndStrengthPower,
)
from .godmode_power import GodmodePower
from .modify_rain_power import ModifyRainPower
from .modify_time_rate_power import ModifyTimeRatePower
from .modify_wind_direction_and_strength_power import (
    ModifyWindDirectionAndStrengthPower,
)
from .spawn_rate_slider_per_player_power import SpawnRateSliderPerPlayerPower
from .start_day_immediately_power import StartDayImmediatelyPower
from .start_midnight_immediately_power import StartMidnightImmediatelyPower
from .start_night_immediately_power import StartNightImmediatelyPower
from .start_noon_immediately_power import StartNoonImmediatelyPower
from .stop_biome_spread_power import StopBiomeSpreadPower

CREATIVE_POWER_REGISTRY: dict[int, type] = {
    0: FreezeTimePower,
    1: StartDayImmediatelyPower,
    2: StartNoonImmediatelyPower,
    3: StartNightImmediatelyPower,
    4: StartMidnightImmediatelyPower,
    5: GodmodePower,
    6: ModifyWindDirectionAndStrengthPower,
    7: ModifyRainPower,
    8: ModifyTimeRatePower,
    9: FreezeRainPower,
    10: FreezeWindDirectionAndStrengthPower,
    11: FarPlacementRangePower,
    12: DifficultySliderPower,
    13: StopBiomeSpreadPower,
    14: SpawnRateSliderPerPlayerPower,
}
