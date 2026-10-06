import mlflow
import pandas as pd


def get_runs():
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    experiment = mlflow.get_experiment_by_name(
        "iris-hyperparameter-tuning"
    )

    if experiment is None:
        raise ValueError(
            "Experiment 'iris-hyperparameter-tuning' not found."
        )

    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time ASC"]
    )

    return runs


def compare_results():
    runs = get_runs()

    selected_runs = runs[
        runs["tags.mlflow.runName"].isin(
            [
                "baseline_decision_tree",
                "grid_search_random_forest",
                "random_search_random_forest",
            ]
        )
    ]

    comparison = selected_runs[
        [
            "tags.mlflow.runName",
            "metrics.cv_f1_macro_mean",
            "metrics.best_cv_f1_macro",
            "metrics.test_accuracy",
        ]
    ].copy()

    comparison["CV F1 Macro"] = comparison[
        "metrics.cv_f1_macro_mean"
    ].fillna(
        comparison["metrics.best_cv_f1_macro"]
    )

    comparison["Test Accuracy"] = comparison[
        "metrics.test_accuracy"
    ]

    comparison = comparison.dropna(subset=["CV F1 Macro", "Test Accuracy"])

    comparison = comparison[
        [
            "tags.mlflow.runName",
            "CV F1 Macro",
            "Test Accuracy",
        ]
    ]

    comparison.columns = [
        "Method",
        "CV F1 Macro",
        "Test Accuracy",
    ]

    print("\n=== Model Comparison ===")
    print(comparison.to_string(index=False))

    comparison.to_csv(
        "tuning_comparison.csv",
        index=False
    )

    print("\nComparison saved to tuning_comparison.csv")


if __name__ == "__main__":
    compare_results()
