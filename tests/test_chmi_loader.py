import pathlib
import pandera.errors
import pytest

from weatherlyser import loader

RUZYNE_PATH = pathlib.Path(__file__).parent / "data" / "P1PRUZ01.xlsx"
RUZYNE_CORRUPT_PATH = pathlib.Path(__file__).parent / "data" / "P1PRUZ01corrupt.xlsx"


def test_load_chmi() -> None:
    # function already decorated with pa.check_types
    # so we just do a simple happy path test
    df = loader.load_chmi_data(RUZYNE_PATH)
    assert not df.empty


def test_load_chmi_pa_validate_error() -> None:
    with pytest.raises(pandera.errors.SchemaError):
        loader.load_chmi_data(RUZYNE_CORRUPT_PATH)
