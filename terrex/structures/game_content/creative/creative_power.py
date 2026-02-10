from dataclasses import dataclass
from typing import Optional
from terrex.util.streamer import Reader, Writer

@dataclass
class CreativePower:
    power_id: int  # 0-14
    enabled: Optional[bool] = None
    slider_current_value_cache: Optional[float] = None

    @classmethod
    def read(cls, reader: Reader) -> 'CreativePower':
        power_id = reader.read_byte()
        cp = cls(power_id=power_id)
        if power_id == 0:
            # FreezeTime
            cp.enabled = reader.read_bool()
        elif power_id == 1:
            # StartDayImmediately (SkipToTime=0)
            pass
        elif power_id == 2:
            # StartNoonImmediately (SkipToTime=27000)
            pass
        elif power_id == 3:
            # StartNightImmediately (SkipToTime=0)
            pass
        elif power_id == 4:
            # StartMidnightImmediately (SkipToTime=16200)
            pass
        elif power_id == 5:
            # GodmodePower
            cp.enabled = reader.read_bool() # godmodePowerEnabled
        elif power_id == 6:
            # ModifyWindDirectionAndStrength
            pass
        elif power_id == 7:
            # ModifyRainPower
            pass
        elif power_id == 8:
            # ModifyTimeRate
            cp.slider_current_value_cache = reader.read_single()
        elif power_id == 9:
            # FreezeRainPower
            cp.enabled = reader.read_bool()
        elif power_id == 10:
            # FreezeWindDirectionAndStrength
            cp.enabled = reader.read_bool()
        elif power_id == 11:
            # FarPlacementRangePower
            cp.enabled = reader.read_bool() # farPlacementRangePowerEnabled
        elif power_id == 12:
            # DifficultySliderPower
            cp.slider_current_value_cache = reader.read_single()
        elif power_id == 13:
            # StopBiomeSpreadPower
            cp.enabled = reader.read_bool()
        elif power_id == 14:
            # SpawnRateSliderPerPlayerPower
            cp.slider_current_value_cache = reader.read_single() # spawnRatePowerSliderValue
        else:
            raise ValueError(f"Unknown CreativePower variant: {power_id}")
        return cp

    def write(self, writer: Writer) -> None:
        writer.write_byte(self.power_id)
        if self.power_id == 0:
            assert self.enabled is not None
            writer.write_bool(self.enabled)
        elif self.power_id == 5:
            assert self.enabled is not None
            writer.write_bool(self.enabled)
        elif self.power_id == 8:
            assert self.slider_current_value_cache is not None
            writer.write_single(self.slider_current_value_cache)
        elif self.power_id == 9:
            assert self.enabled is not None
            writer.write_bool(self.enabled)
        elif self.power_id == 10:
            assert self.enabled is not None
            writer.write_bool(self.enabled)
        elif self.power_id == 11:
            assert self.enabled is not None
            writer.write_bool(self.enabled)
        elif self.power_id == 12:
            assert self.slider_current_value_cache is not None
            writer.write_single(self.slider_current_value_cache)
        elif self.power_id == 13:
            assert self.enabled is not None
            writer.write_bool(self.enabled)
        elif self.power_id == 14:
            assert self.slider_current_value_cache is not None
            writer.write_single(self.slider_current_value_cache)
        # Other variants have no data