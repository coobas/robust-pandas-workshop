"""Support module for loading data from Open Meteo API and other sources

This module is not to be modified during the workshop.
"""

import gzip
import hashlib
import json
import pathlib
import pickle
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

import httpx
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from weatherlyser import api_models, pa_models

CACHE_DIR = pathlib.Path.cwd() / "cache"
CACHE_DIR.mkdir(exist_ok=True)

ARCHIVE_URI = "https://archive-api.open-meteo.com/v1/archive"


P = ParamSpec("P")
T = TypeVar("T")


def memoize_to_file(func: Callable[P, T]) -> Callable[P, T]:
    """Memoize function results to file

    This helps us save results locally so we do not put too much load on the API.
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Create a unique file name based on the function name and arguments
        key = hashlib.md5(pickle.dumps((func.__name__, args, kwargs))).hexdigest()

        filepath = CACHE_DIR / f"{func.__name__}_{key}.json.gz"

        # Check if the file already exists and return the cached result if it does
        if filepath.exists():
            with gzip.open(filepath, "rb") as f:
                return json.load(f)

        # Call the function and store the result in a file
        result = func(*args, **kwargs)
        with gzip.open(filepath, "wt") as f:
            json.dump(result, f)

        return result

    return wrapper


@memoize_to_file
def httpx_get_json(uri: str, params: dict) -> Any:
    """Cached httpx.get request

    Cache data can be provided upfront to save the number of API calls.
    """
    response = httpx.get(uri, params=params)
    response.raise_for_status()
    return response.json()


def load_open_meteo_archive_data(
    params: api_models.ArchiveQueryParameters,
) -> api_models.V1ArchiveGetResponse:
    """Load data from the archive API

    Args:
        params (models.ArchiveQueryParameters): [description]

    Returns:
        models.V1ArchiveGetResponse: [description]
    """
    data = httpx_get_json(ARCHIVE_URI, params=params.dict(exclude_unset=True))
    return api_models.V1ArchiveGetResponse.parse_obj(data)


CZ_EN_TRANSLATION = {
    "teplota průměrná": "average temperature",
    "teplota maximální": "maximum temperature",
    "teplota minimální": "minimum temperature",
    "rychlost větru": "wind speed",
    "tlak vzduchu": "air pressure",
    "vlhkost vzduchu": "humidity",
    "úhrn srážek": "precipitation",
    "celková výška sněhu": "total snow depth",
    "sluneční svit": "sunshine",
}


DEFAULT_CHMI_DATA_PATH = pathlib.Path(__file__).parent.parent / "data" / "P1PRUZ01.xlsx"

# Solution to exercise in Data loading module
@pa.check_types
def load_chmi_data(
    path: str | pathlib.Path = DEFAULT_CHMI_DATA_PATH,
) -> DataFrame[pa_models.CHMIDailyDataFrame]:
    """Load historical weather data from ČHMÚ"""
    excel_data = pd.ExcelFile(path)

    # Read all sheets but the first one
    extracted_sheets = [
        extract_and_clean_chmi_excel_sheet(excel_data, sheet_name)
        for sheet_name in excel_data.sheet_names[1:]
    ]
    result = (
        pd.concat(extracted_sheets, axis=1)
        .rename(columns=CZ_EN_TRANSLATION)
        .rename(columns=lambda c: c.replace(" ", "_"))
    )
    return result


def extract_and_clean_chmi_excel_sheet(
    excel_data: pd.ExcelFile, sheet_name: int | str
) -> pd.DataFrame:
    """Parse ČHMÚ historical meteo excel data"""
    data_tidy = (
        excel_data.parse(sheet_name, skiprows=3)
        .melt(id_vars=["rok", "měsíc"], var_name="den", value_name=sheet_name)
        .dropna()
    )
    dates = pd.to_datetime(
        data_tidy[["rok", "měsíc", "den"]].rename(
            columns={"rok": "year", "měsíc": "month", "den": "day"}
        )
    )
    return (
        data_tidy.assign(date=dates)
        .set_index("date")
        .drop(columns=["rok", "měsíc", "den"])
        .sort_index()
    )
