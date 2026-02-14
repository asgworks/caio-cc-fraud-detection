"""
Fraud Detection Feature Definitions for Feast
"""
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, FeatureService
from feast.types import Float32, Int64, String
from feast.value_type import ValueType

# Define entities with value_type
transaction = Entity(
    name="transaction",
    join_keys=["trans_num"],
    description="Transaction identifier",
    value_type=ValueType.STRING
)

customer = Entity(
    name="customer",
    join_keys=["cc_num"],
    description="Credit card number (customer identifier)",
    value_type=ValueType.STRING
)

merchant = Entity(
    name="merchant",
    join_keys=["merchant"],
    description="Merchant identifier",
    value_type=ValueType.STRING
)

# Transaction features data source (with timestamps!)
transaction_source = FileSource(
    name="transaction_features_source",
    path="../data/processed/X_train_with_timestamps.parquet",
    timestamp_field="timestamp",
)

# Transaction feature view - basic transaction features
transaction_features = FeatureView(
    name="transaction_features",
    entities=[transaction],
    ttl=timedelta(days=365),
    schema=[
        Field(name="amt", dtype=Float32, description="Transaction amount"),
        Field(name="city_pop", dtype=Int64, description="City population"),
        Field(name="category_encoded", dtype=Int64, description="Transaction category"),
        Field(name="gender_encoded", dtype=Int64, description="Customer gender"),
        Field(name="state_encoded", dtype=Int64, description="State code"),
    ],
    online=True,
    source=transaction_source,
    tags={"team": "fraud_detection", "type": "transaction"},
)

# Feature service for fraud detection model
fraud_detection_v1 = FeatureService(
    name="fraud_detection_v1",
    features=[transaction_features],
    description="Fraud detection features v1 - basic transaction data"
)
