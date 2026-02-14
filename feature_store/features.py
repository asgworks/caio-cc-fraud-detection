"""
Fraud Detection Feature Definitions for Feast

NOTE: This is a simplified version that uses basic transaction features.
The current data (X_train.csv) doesn't have timestamp columns yet.
To use Feast properly, you'll need to:
1. Add timestamp columns to your data
2. Create aggregated feature files (customer_aggregates, merchant_aggregates)

For now, this file shows the structure but may not work with `feast apply`
until the data is properly prepared.
"""
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, FeatureService
from feast.types import Float32, Int64, String

# Note: Feast requires timestamps in data sources
# Your current X_train.csv doesn't have timestamps
# This is a template showing how features SHOULD be defined

# For a working example, you would need to:
# 1. Add a timestamp column to your processed data
# 2. Use the raw data (fraudTrain.csv) which has trans_date_trans_time

# Example of what the features would look like:
"""
# Entities with value_type specified
transaction = Entity(
    name="transaction",
    join_keys=["trans_num"],
    description="Transaction identifier",
    value_type=String
)

# Basic transaction features using existing columns
transaction_source = FileSource(
    name="transaction_features_source",
    path="../data/processed/X_train.csv",
    # Note: X_train.csv doesn't have a timestamp field
    # You'll need to add one or use raw data
)

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
    tags={"team": "fraud_detection", "type": "basic"},
)

fraud_detection_v1 = FeatureService(
    name="fraud_detection_v1",
    features=[transaction_features],
    description="Basic fraud detection features"
)
"""

# Placeholder - actual features commented out until data has timestamps
print("Feature definitions are templates only.")
print("Your data needs timestamp columns before Feast can be used.")
print("See notebooks/05_feature_store.ipynb for guidance on preparing data.")
