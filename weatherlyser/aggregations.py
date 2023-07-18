import pandera as pa

from pandera import Float
from pandera.typing import DataFrame


class TemperatureModel(pa.DataFrameModel):
    temperature_2m: Float = pa.Field(ge=-100, le=100, nullable=True)
    # time: Index[Annotated[pd.DatetimeTZDtype, "ns", "UTC"]]


class DailyTemperatureModel(pa.DataFrameModel):
    temperature_2m_min: Float = pa.Field(nullable=True)
    temperature_2m_mean: Float = pa.Field(nullable=True)
    temperature_2m_max: Float = pa.Field(nullable=True)

    # time: Dat[Annotated[pd.DatetimeTZDtype, "ns", "UTC"]]


@pa.check_types
def get_daily_temperature_stats(df: DataFrame[TemperatureModel]) -> DataFrame[DailyTemperatureModel]:
    # Note: We will need this in further analyses
    df = (
        df
        .reset_index(level="model")
        .groupby("model")
        .resample("D")
        ["temperature_2m"]
        .agg(["min", "mean", "max"])
        .rename(columns = lambda n: f"temperature_2m_{n}")
        .reorder_levels(["time", "model"])
        .sort_index()
    )
    df = df.set_index(df.index.rename(["date", "model"]))
    return df
