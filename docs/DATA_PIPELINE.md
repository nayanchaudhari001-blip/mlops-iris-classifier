# Data Pipeline Documentation

## Overview

This project implements an end-to-end MLOps data pipeline using DVC.
The pipeline contains four stages:

**Collect → Preprocess → Features → Validate**

DVC manages the dependencies, outputs, caching, and reproducibility of each stage.

---

## 1. Data Collection

### Purpose
Collect the Iris dataset and store it in the raw data zone.

### Input
External Iris dataset from `scikit-learn`.

### Output
`data/raw/iris_raw.csv`

### Processing
- Loads the Iris dataset.
- Converts target numbers into species names.
- Adds collection timestamp metadata.
- Saves 150 records.

---

## 2. Data Preprocessing

### Purpose
Clean and prepare the collected data for feature engineering.

### Input
`data/raw/iris_raw.csv`

### Output
`data/processed/iris_preprocessed.csv`

### Processing
- Removes duplicate records.
- Converts numeric columns to numeric types.
- Handles missing numeric values using column median.
- Removes rows with missing target values.
- Removes the `collected_at` metadata column.

### Result
149 rows were produced after removing 1 duplicate record.

---

## 3. Feature Engineering

### Purpose
Create additional model-useful features from the cleaned Iris measurements.

### Input
`data/processed/iris_preprocessed.csv`

### Output
`data/processed/iris_features.csv`

### Features Created

- `sepal_area`
- `petal_area`
- `sepal_to_petal_length_ratio`
- `petal_length_bin`

The final dataset contains 149 rows and 9 columns.

---

## 4. Data Validation

### Purpose
Verify that the processed feature dataset satisfies the required schema and statistical rules before being used downstream.

### Input
`data/processed/iris_features.csv`

### Validation Rules

#### Schema Validation
- All expected columns must be present.
- No unexpected null values are allowed.
- Species must be one of:
  - `setosa`
  - `versicolor`
  - `virginica`

#### Range Validation
- Sepal length: 3.0–9.0
- Sepal width: 1.5–5.5
- Petal length: 0.5–8.0
- Petal width: 0.05–3.0

If any validation check fails, the pipeline stops with a non-zero exit code.

---

## 5. DVC Pipeline

The pipeline is defined in `dvc.yaml`.

### Pipeline Flow

```text
Raw Source
    |
    v
+-----------+
|  Collect  |
+-----------+
    |
    v
+-------------+
| Preprocess  |
+-------------+
    |
    v
+------------+
|  Features  |
+------------+
    |
    v
+------------+
|  Validate  |
+------------+
    |
    v
Validated Feature Data