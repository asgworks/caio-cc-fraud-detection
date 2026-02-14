# Feature Store

This directory contains the Feast feature store configuration for the fraud detection project.

## Structure

- `feature_store.yaml` - Feature store configuration
- `features.py` - Feature definitions (entities, feature views, feature services)
- `data/` - Local storage for registry and online store

## Setup

1. **Apply feature definitions**:
```bash
cd feature_store
feast apply
```

2. **Verify setup**:
```bash
feast feature-views list
feast feature-services list
```

## Usage

### From Python

```python
from src.features import get_fraud_feature_store

# Initialize
fs = get_fraud_feature_store()

# Get historical features for training
entity_df = pd.DataFrame({
    'trans_num': [...],
    'timestamp': [...]
})
features = fs.get_historical_features(
    entity_df=entity_df,
    features=["fraud_detection_v1"]
)

# Materialize to online store
fs.materialize(start_date='2024-01-01', end_date='2024-12-31')

# Get online features for prediction
online_features = fs.get_online_features(
    entity_rows=[{'trans_num': 'txn_001', ...}],
    features=["fraud_detection_v1"]
)
```

### From CLI

```bash
# List features
feast feature-views list

# Materialize features
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")

# Materialize specific date range
feast materialize 2024-01-01T00:00:00 2024-12-31T23:59:59
```

## Feature Views

1. **transaction_features** - Basic transaction data (amount, location, etc.)
2. **customer_features** - Customer aggregates (transaction counts, amounts over time windows)
3. **merchant_features** - Merchant statistics (fraud rate, average amounts)

## Feature Service

**fraud_detection_v1** - Combines all feature views for the fraud detection model

## Notes

- The current configuration uses local file storage (SQLite) for development
- For production, consider using cloud-based stores (Snowflake, BigQuery, Redshift)
- Make sure to create the aggregated feature files before materializing
