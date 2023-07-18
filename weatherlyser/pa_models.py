import pandera as pa
from pandera.typing import Index, Series
from typing import Annotated, Optional
import pandas as pd


class HistoricalWeatherDataFrame(pa.DataFrameModel):
    apparent_temperature: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    cloudcover: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    cloudcover_high: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    cloudcover_low: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    cloudcover_mid: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    dewpoint_2m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    diffuse_radiation: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    direct_normal_irradiance: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    direct_radiation: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    et0_fao_evapotranspiration: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    precipitation: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    pressure_msl: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    rain: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    relativehumidity_2m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    shortwave_radiation: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    snowfall: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    soil_moisture_0_to_7cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    soil_moisture_100_to_255cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    soil_moisture_28_to_100cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    soil_moisture_7_to_28cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    soil_temperature_0_to_7cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    soil_temperature_100_to_255cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    soil_temperature_28_to_100cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    soil_temperature_7_to_28cm: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    temperature_2m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    vapor_pressure_deficit: Optional[Series[float]] = pa.Field(
        nullable=True, coerce=True
    )
    weathercode: Optional[Series[pd.Int16Dtype]] = pa.Field(nullable=True, coerce=True)
    winddirection_100m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    winddirection_10m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    windgusts_10m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    windspeed_100m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    windspeed_10m: Optional[Series[float]] = pa.Field(nullable=True, coerce=True)
    is_day: Optional[Series[bool]] = pa.Field(nullable=True, coerce=True)

    time: Index[Annotated[pd.DatetimeTZDtype, "ns", "UTC"]]
    model: Index[str]


# Solution to exercise in Data loading module
class CHMIDailyDataFrame(pa.DataFrameModel):
    average_temperature: Series[float] = pa.Field(coerce=True)
    maximum_temperature: Series[float] = pa.Field(coerce=True)
    minimum_temperature: Series[float] = pa.Field(coerce=True)
    wind_speed: Series[float] = pa.Field(coerce=True)
    air_pressure: Series[float] = pa.Field(coerce=True)
    humidity: Series[float] = pa.Field(coerce=True)
    precipitation: Series[float] = pa.Field(coerce=True)
    total_snow_depth: Series[float] = pa.Field(coerce=True)
    sunshine: Series[float] = pa.Field(coerce=True)
    date: Index[Annotated[pd.DatetimeTZDtype, "ns", "Europe/Prague"]]


WEATHER_CODES = {
    # From https://open-meteo.com/en/docs
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle, light intensity",
    53: "Drizzle, moderate intensity",
    55: "Drizzle, dense intensity",
    56: "Freezing drizzle, light intensity",
    57: "Freezing drizzle, dense intensity",
    61: "Rain, slight intensity",
    63: "Rain, moderate intensity",
    65: "Rain, heavy intensity",
    66: "Freezing rain, light intensity",
    67: "Freezing rain, heavy intensity",
    71: "Snow fall, slight intensity",
    73: "Snow fall, moderate intensity",
    75: "Snow fall, heavy intensity",
    77: "Snow grains",
    80: "Rain showers, slight intensity",
    81: "Rain showers, moderate intensity",
    82: "Rain showers, violent intensity",
    85: "Snow showers slight intensity",
    86: "Snow showers heavy intensity",
    95: "Thunderstorm, slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}
