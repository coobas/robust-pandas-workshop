from collections.abc import Iterable
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from weatherlyser import api_models, pa_models
from weatherlyser.loader import load_open_meteo_archive_data


# Exercise: write a pa schema for get_seasons output
# add check output decorator
# create tests for the schema (pytest.raises)
# create hypothesis tests (happy path)

seasons_series_schema = pa.SeriesSchema(
    pa.String,
    checks=[
        pa.Check.isin({"winter", "spring", "summer", "autumn"}),
    ],
    nullable=False,
    index=pa.Index(dt.datetime),
)


@pa.check_output(seasons_series_schema)
def get_seasons(time_index: pd.DatetimeIndex) -> pd.Series:
    """Returns a series the meteorological seasons for the given time index."""
    seasons = pd.Series(index=time_index, dtype="string")
    seasons.loc[time_index.month.isin([12, 1, 2])] = "winter"
    seasons.loc[time_index.month.isin([3, 4, 5])] = "spring"
    seasons.loc[time_index.month.isin([6, 7, 8])] = "summer"
    seasons.loc[time_index.month.isin([9, 10, 11])] = "autumn"
    return seasons


def open_meteo_response_to_dataframe(
    data: api_models.V1ArchiveGetResponse, tz: str | dt.timezone | None = None
) -> pd.DataFrame:
    """Convert Open Meteo API response to a dataframe"""

    # *** This would be a good task
    if data.utc_offset_seconds is None:
        if tz is None:
            raise ValueError("utc_offset_seconds is None - timezone is not set")
    elif tz is None:
        tz = dt.timezone(dt.timedelta(seconds=data.utc_offset_seconds))

    df = pd.DataFrame(data.hourly)
    df = df.assign(
        time=pd.to_datetime(df["time"]).dt.tz_localize(
            # explict tz like Europe/Prague can actually cause an issue
            # because the API returns times with *fixed* UTC offset
            tz
        ),
    ).set_index("time")
    return df


# Exercise solution:

_open_meteo_df_schema_extra_columns_types = {
    "is_day": pa.Column(bool, nullable=True, coerce=True, regex=True, required=False),
    "weathercode": pa.Column(pd.Int16Dtype, nullable=True, coerce=True, regex=True, required=False),
}

open_meteo_df_schema = pa.DataFrameSchema(
    {
        (
            "^("
            + "|".join(
                variable.name
                for variable in api_models.HourlyEnum
                if variable.name not in _open_meteo_df_schema_extra_columns_types
            )
            + ")_("
            + "|".join(model.name for model in api_models.HistoryModelsEnum)
            + ")$"
        ): pa.Column(
            float,
            regex=True,
            nullable=True,
            coerce=True,
            required=False,
        ),
    },
    index=pa.Index(pd.DatetimeTZDtype("ns", "UTC"), unique=True, name="time"),
    strict=True,
)

open_meteo_df_schema = open_meteo_df_schema.add_columns(
    {
        (
            f"^({quantity})"
            + "_("
            + "|".join(model.name for model in api_models.HistoryModelsEnum)
            + ")$"
        ): column
        for quantity, column in _open_meteo_df_schema_extra_columns_types.items()
    }
)

# Exercise 2: write property based tests for tidy_open_meteo_dataframe
# will be interesting to see how the regex works with hypothesis
# maybe will need to add custom strategy:
# https://pandera.readthedocs.io/en/stable/extensions.html#specifying-a-check-strategy


# TODO: Loading does not work for me with this
@pa.check_input(open_meteo_df_schema, "df")
@pa.check_types
def tidy_open_meteo_dataframe(
    df: pd.DataFrame,
) -> DataFrame[pa_models.HistoricalWeatherDataFrame]:
    # *** This would be a good task
    pattern = (
        "^("
        + "|".join(variable.name for variable in api_models.HourlyEnum)
        + ")_("
        + "|".join(model.name for model in api_models.HistoryModelsEnum)
        + ")$"
    )
    # check that all columns match the pattern
    # Exercise: make this a pandera check
    if not df.columns.str.match(pattern).all():
        raise ValueError(
            f"Unexpected columns in the dataframe: {df.columns[~df.columns.str.match(pattern)].to_list()}"
        )
    new_columns = pd.MultiIndex.from_frame(
        df.columns.str.extract(pattern, expand=True), names=["quantity", "model"]
    )
    result = df.set_axis(new_columns, axis="columns").stack(level="model")
    return result


def _create_archive_query_parameters(
    *,
    start_date: dt.date | pd.Timestamp,
    end_date: dt.date | pd.Timestamp,
    latitude: float,
    longitude: float,
    models: Iterable[str],
    fields: Iterable[str],
) -> api_models.ArchiveQueryParameters:
    return api_models.ArchiveQueryParameters(
        latitude=latitude,
        longitude=longitude,
        hourly=list(fields),
        start_date=pd.Timestamp(start_date),
        end_date=pd.Timestamp(end_date),
        models=list(models),
    )


PRAGUE_LATITUDE = 50.1003
PRAGUE_LONGITUDE = 14.2555
DEFAULT_MODELS = "best_match", "era5", "era5_land", "cerra"
DEFAULT_FIELDS = [
    "temperature_2m",
    "relativehumidity_2m",
    "dewpoint_2m",
    "apparent_temperature",
    "precipitation",
    "rain",
    # "showers",
    "snowfall",
    "weathercode",
    "pressure_msl",
    "surface_pressure",
    "cloudcover",
    "cloudcover_low",
    "cloudcover_mid",
    "cloudcover_high",
    "et0_fao_evapotranspiration",
    "vapor_pressure_deficit",
    "windspeed_10m",
    "windspeed_100m",
    "winddirection_10m",
    "winddirection_100m",
    "windgusts_10m",
    "soil_temperature_0_to_7cm",
    "soil_temperature_7_to_28cm",
    "soil_temperature_28_to_100cm",
    "soil_temperature_100_to_255cm",
    "soil_moisture_0_to_7cm",
    "soil_moisture_7_to_28cm",
    "soil_moisture_28_to_100cm",
    "soil_moisture_100_to_255cm",
    "is_day",
    "shortwave_radiation",
    "direct_radiation",
    "diffuse_radiation",
    "direct_normal_irradiance",
]


@pa.check_types
def get_open_meteo_data(
    start_date: str | dt.date | pd.Timestamp,
    end_date: str | dt.date | pd.Timestamp,
    *,
    chunk_size: relativedelta | dt.timedelta | pd.Timedelta = relativedelta(months=1),
    latitude: float = PRAGUE_LATITUDE,
    longitude: float = PRAGUE_LONGITUDE,
    models: Iterable[str] = DEFAULT_MODELS,
    fields: Iterable[str] = DEFAULT_FIELDS,
) -> DataFrame[pa_models.HistoricalWeatherDataFrame]:
    """Retrieve data for the specified date range and place."""

    # We take a bit longer interval to work properly with dates
    start_timestamp, end_timestamp = pd.Timestamp(start_date), pd.Timestamp(
        end_date
    ) + dt.timedelta(days=1)
    chunk_end = start_timestamp

    chunk_dfs = []
    while (chunk_start := chunk_end) < end_timestamp:
        chunk_end = min(chunk_start + chunk_size, end_timestamp)
        query_parameters = _create_archive_query_parameters(
            start_date=chunk_start,
            end_date=chunk_end,
            latitude=latitude,
            longitude=longitude,
            models=models,
            fields=fields,
        )
        response = load_open_meteo_archive_data(query_parameters)
        original_df = open_meteo_response_to_dataframe(response)
        tidy_df = tidy_open_meteo_dataframe(original_df)
        chunk_dfs.append(tidy_df)

    # The limits are somewhat fuzzy & overlapping, use the logic used by pandas
    return pd.concat(chunk_dfs, axis="rows").drop_duplicates().loc[start_date:end_date]  # type: ignore
