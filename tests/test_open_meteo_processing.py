import pathlib

import hypothesis
import pandas as pd
import pandera.errors
import pytest

from weatherlyser import processors


class TestTidyOpenMeteoDataframe:
    @hypothesis.given(
        df=processors.open_meteo_df_schema.strategy(n_regex_columns=2, size=None),
    )
    @hypothesis.example(
        pd.read_parquet(
            pathlib.Path(__file__).parent / "data" / "open_meteo_wide_example_1.parquet"
        )
    )
    @hypothesis.example(
        pd.read_parquet(
            pathlib.Path(__file__).parent / "data" / "open_meteo_wide_example_2.parquet"
        )
    )
    # n_regex_columns generates that number of columns per every single regex
    # so 2 regex columns means 6 columns in total
    # large number makes hypothesis unhappy
    def test_valid_schema(self, df: pd.DataFrame) -> None:
        processors.tidy_open_meteo_dataframe(df)

    @hypothesis.given(
        df=processors.open_meteo_df_schema.strategy(n_regex_columns=1, size=2)
    )
    @hypothesis.settings(max_examples=2)
    def test_invalid_index(self, df: pd.DataFrame) -> None:
        df = df.reset_index(drop=True)
        with pytest.raises(pandera.errors.SchemaError):
            processors.tidy_open_meteo_dataframe(df)

    @hypothesis.given(
        df=processors.open_meteo_df_schema.strategy(n_regex_columns=1, size=2)
    )
    @hypothesis.settings(max_examples=2)
    def test_invalid_columns(self, df: pd.DataFrame) -> None:
        df = df.assign(invalid_column=1.23)
        with pytest.raises(pandera.errors.SchemaError):
            processors.tidy_open_meteo_dataframe(df)
