"""
MLflow utilities for fraud detection project
"""
import mlflow
import mlflow.sklearn
from typing import Dict, Any, Optional


def setup_mlflow(tracking_uri: str = "./mlruns", experiment_name: str = "fraud_detection"):
    """
    Setup MLflow tracking
    
    Args:
        tracking_uri: URI for MLflow tracking server
        experiment_name: Name of the experiment
    """
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    
    experiment = mlflow.get_experiment_by_name(experiment_name)
    print(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
    print(f"Experiment ID: {experiment.experiment_id}")
    print(f"Experiment Name: {experiment.name}")


def log_model_params(params: Dict[str, Any]):
    """
    Log model parameters to MLflow
    
    Args:
        params: Dictionary of parameters
    """
    mlflow.log_params(params)


def log_dataset_info(X_train, y_train):
    """
    Log dataset information to MLflow
    
    Args:
        X_train: Training features
        y_train: Training labels
    """
    mlflow.log_param("train_samples", len(X_train))
    mlflow.log_param("n_features", X_train.shape[1])
    mlflow.log_param("fraud_rate", y_train.mean())


def log_metrics(metrics: Dict[str, float]):
    """
    Log metrics to MLflow
    
    Args:
        metrics: Dictionary of metric names and values
    """
    mlflow.log_metrics(metrics)


def register_model(model, model_name: str = "fraud_detector", artifact_path: str = "model"):
    """
    Log and register model in MLflow
    
    Args:
        model: Trained model
        model_name: Name for model registry
        artifact_path: Path to save model artifact
    
    Returns:
        Model info
    """
    return mlflow.sklearn.log_model(
        model,
        artifact_path,
        registered_model_name=model_name
    )


def load_production_model(model_name: str = "fraud_detector", stage: str = "Production"):
    """
    Load model from MLflow registry
    
    Args:
        model_name: Name of the registered model
        stage: Model stage (None, Staging, Production, Archived)
    
    Returns:
        Loaded model
    """
    model_uri = f"models:/{model_name}/{stage}"
    return mlflow.pyfunc.load_model(model_uri)


def get_latest_run(experiment_name: str = "fraud_detection"):
    """
    Get the latest run from an experiment
    
    Args:
        experiment_name: Name of the experiment
    
    Returns:
        Latest run info or None
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment:
        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
            max_results=1
        )
        if not runs.empty:
            return runs.iloc[0]
    return None
