
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def create_dataset():
    rng = np.random.default_rng(42)

    X = pd.DataFrame(
        rng.normal(5, 1, (30, 4)),
        columns=[
            "sepal length (cm)",
            "sepal width (cm)",
            "petal length (cm)",
            "petal width (cm)",
        ],
    )

    y = rng.integers(0, 3, size=30)

    return X, y


def test_model_trains_successfully():
    X, y = create_dataset()

    model = RandomForestClassifier(
        n_estimators=10,
        random_state=42,
    )
    model.fit(X, y)

    assert hasattr(model, "predict")


def test_model_predictions_have_correct_shape():
    X, y = create_dataset()

    model = RandomForestClassifier(
        n_estimators=10,
        random_state=42,
    )
    model.fit(X, y)

    predictions = model.predict(X)

    assert predictions.shape == (30,)


def test_model_prediction_probabilities_sum_to_one():
    X, y = create_dataset()

    model = RandomForestClassifier(
        n_estimators=10,
        random_state=42,
    )
    model.fit(X, y)

    probabilities = model.predict_proba(X)

    assert probabilities.shape == (30, 3)
    assert np.allclose(probabilities.sum(axis=1), 1.0)
