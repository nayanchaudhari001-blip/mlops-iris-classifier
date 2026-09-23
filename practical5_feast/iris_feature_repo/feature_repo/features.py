from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource, FeatureService
from feast.types import Float32, String


sample = Entity(
    name="sample_id",
    join_keys=["sample_id"],
)

iris_source = FileSource(
    name="iris_features_source",
    path="data/iris_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

iris_measurements = FeatureView(
    name="iris_measurements",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[
        Field(name="sepal length (cm)", dtype=Float32),
        Field(name="sepal width (cm)", dtype=Float32),
        Field(name="petal length (cm)", dtype=Float32),
        Field(name="petal width (cm)", dtype=Float32),
    ],
    source=iris_source,
    online=True,
)

iris_engineered_features = FeatureView(
    name="iris_engineered_features",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[
        Field(name="sepal_area", dtype=Float32),
        Field(name="petal_area", dtype=Float32),
        Field(name="sepal_to_petal_length_ratio", dtype=Float32),
        Field(name="petal_length_bin", dtype=String),
    ],
    source=iris_source,
    online=True,
)

iris_feature_service = FeatureService(
    name="iris_feature_service",
    features=[
        iris_measurements,
        iris_engineered_features,
    ],
)
