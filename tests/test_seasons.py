import datetime as dt

import pandas as pd
import pandera.errors
from hypothesis import given
import pytest

from weatherlyser import pa_models, processors


@given(data=pa_models.CHMIDailyDataFrame.strategy())
def test_get_seasons(data: pd.DataFrame) -> None:
    seasons = processors.get_seasons(data.index)
    assert seasons.isin(["winter", "spring", "summer", "autumn"]).all()


@pytest.fixture
def valid_seasons() -> pd.Series:
    return pd.Series(
        ["winter", "spring", "summer", "autumn"],
        index=[
            dt.datetime(2022, 1, 1),
            dt.datetime(2022, 4, 1),
            dt.datetime(2022, 7, 1),
            dt.datetime(2022, 10, 1),
        ],
    )


@pytest.fixture
def invalid_seasons() -> pd.Series:
    return pd.Series(
        ["winter", "spring", "fall", "summer"],
        index=[
            dt.datetime(2022, 1, 1),
            dt.datetime(2022, 4, 1),
            dt.datetime(2022, 7, 1),
            dt.datetime(2022, 10, 1),
        ],
    )


def test_seasons_series_schema_valid(valid_seasons: pd.Series) -> None:
    pd.testing.assert_series_equal(
        processors.seasons_series_schema.validate(valid_seasons), valid_seasons
    )


def test_seasons_series_schema_invalid(invalid_seasons: pd.Series) -> None:
    with pytest.raises(pandera.errors.SchemaError):
        processors.seasons_series_schema.validate(invalid_seasons)
