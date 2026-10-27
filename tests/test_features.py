import pandas as pd
import numpy as np
from src.pipeline.features import engineer_features


def create_test_csv(tmp_path, data):
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"

    df = pd.DataFrame(data)
    df.to_csv(input_path, index=False)

    return str(input_path), str(output_path)


def test_engineer_features_creates_expected_columns(tmp_path):
    input_path, output_path = create_test_csv(tmp_path, {
        "sepal length (cm)": [5.1],
        "sepal width (cm)": [3.5],
        "petal length (cm)": [1.4],
        "petal width (cm)": [0.2],
        "species": ["setosa"],
    })

    result = engineer_features(input_path, output_path)

    assert "sepal_area" in result.columns
    assert "petal_area" in result.columns
    assert "sepal_to_petal_length_ratio" in result.columns
    assert "petal_length_bin" in result.columns


def test_engineer_features_calculates_values(tmp_path):
    input_path, output_path = create_test_csv(tmp_path, {
        "sepal length (cm)": [5.0],
        "sepal width (cm)": [2.0],
        "petal length (cm)": [4.0],
        "petal width (cm)": [1.0],
        "species": ["versicolor"],
    })

    result = engineer_features(input_path, output_path)

    assert result.loc[0, "sepal_area"] == 10.0
    assert result.loc[0, "petal_area"] == 4.0
    assert result.loc[0, "sepal_to_petal_length_ratio"] == 1.25


def test_petal_length_bin(tmp_path):
    input_path, output_path = create_test_csv(tmp_path, {
        "sepal length (cm)": [5.0, 6.0, 7.0],
        "sepal width (cm)": [3.0, 3.0, 3.0],
        "petal length (cm)": [1.0, 3.0, 5.0],
        "petal width (cm)": [0.2, 1.0, 1.8],
        "species": ["setosa", "versicolor", "virginica"],
    })

    result = engineer_features(input_path, output_path)

    assert result.loc[0, "petal_length_bin"] == "short"
    assert result.loc[1, "petal_length_bin"] == "medium"
    assert result.loc[2, "petal_length_bin"] == "long"


def test_zero_petal_length_does_not_crash(tmp_path):
    input_path, output_path = create_test_csv(tmp_path, {
        "sepal length (cm)": [5.0],
        "sepal width (cm)": [3.0],
        "petal length (cm)": [0.0],
        "petal width (cm)": [0.0],
        "species": ["setosa"],
    })

    result = engineer_features(input_path, output_path)

    assert pd.isna(result.loc[0, "sepal_to_petal_length_ratio"])