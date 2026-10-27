
import pandas as pd
import pytest

from src.pipeline.validate import validate, DataValidationError


def valid_dataframe():
    return pd.DataFrame({
        "sepal length (cm)": [5.1],
        "sepal width (cm)": [3.5],
        "petal length (cm)": [1.4],
        "petal width (cm)": [0.2],
        "species": ["setosa"],
        "sepal_area": [17.85],
        "petal_area": [0.28],
        "sepal_to_petal_length_ratio": [3.64],
        "petal_length_bin": ["short"],
    })


def run_validation(df, tmp_path):
    input_path = tmp_path / "test_data.csv"
    df.to_csv(input_path, index=False)
    return validate(str(input_path))


def test_validate_passes_on_clean_data(tmp_path):
    result = run_validation(valid_dataframe(), tmp_path)
    assert result is not None


def test_validate_fails_on_missing_column(tmp_path):
    df = valid_dataframe().drop(columns=["sepal_area"])

    with pytest.raises(DataValidationError, match="Validation failed"):
        run_validation(df, tmp_path)


def test_validate_fails_on_invalid_species(tmp_path):
    df = valid_dataframe()
    df.loc[0, "species"] = "unicorn"

    with pytest.raises(DataValidationError, match="Validation failed"):
        run_validation(df, tmp_path)


def test_validate_fails_on_out_of_range_value(tmp_path):
    df = valid_dataframe()
    df.loc[0, "sepal length (cm)"] = 50

    with pytest.raises(DataValidationError, match="Validation failed"):
        run_validation(df, tmp_path)
