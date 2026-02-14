# MLflow Integration

## Overview

MLflow is now integrated into the fraud detection project for experiment tracking, model registry, and reproducibility.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MLflow UI:
```bash
./scripts/start_mlflow.sh
# Or manually:
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts
```

3. Access MLflow UI at: http://localhost:5000

## What's Tracked

### During Training (03_modeling.ipynb):
- **Parameters:**
  - Model hyperparameters (max_iter, random_state, solver)
  - Training dataset size
  - Number of features
  - Fraud rate in training data

- **Model:**
  - Trained scikit-learn model
  - Registered in MLflow Model Registry as "fraud_detector"

### During Evaluation (04_model_evaluation.ipynb):
- **Metrics:**
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC AUC

## Usage

### Run Training with MLflow Tracking:
```python
import mlflow

mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment("fraud_detection")

with mlflow.start_run(run_name="my_experiment"):
    # Your training code
    mlflow.log_param("param_name", value)
    mlflow.log_metric("metric_name", value)
    mlflow.sklearn.log_model(model, "model")
```

### Load Model from MLflow:
```python
import mlflow.sklearn

# Load by run_id
model = mlflow.sklearn.load_model("runs:/<run_id>/model")

# Load from registry
model = mlflow.pyfunc.load_model("models:/fraud_detector/Production")
```

## Model Registry

Models are automatically registered as "fraud_detector". You can promote models through stages:

1. **None** - Default stage after registration
2. **Staging** - For testing
3. **Production** - Active production model
4. **Archived** - Retired models

## File Structure

```
mlruns/              # MLflow tracking data
mlartifacts/         # Model artifacts
mlflow.db           # SQLite backend store
mlflow_config.yaml  # MLflow configuration
```

## Next Steps

- Compare multiple experiments in MLflow UI
- Promote best model to Production stage
- Use MLflow Models for serving
- Add more sophisticated models and track their performance
