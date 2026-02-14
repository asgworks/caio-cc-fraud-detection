"""
FastAPI application for fraud detection model serving
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mlflow
import mlflow.sklearn
import numpy as np
from typing import Optional
import logging

from .schemas import TransactionRequest, PredictionResponse, HealthResponse
from src.features import get_fraud_feature_store

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Fraud Detection API",
    description="Real-time fraud detection using MLflow and Feast",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and feature store
model = None
model_version = None
feature_store = None


@app.on_event("startup")
async def startup_event():
    """Load model and initialize feature store on startup"""
    global model, model_version, feature_store
    
    try:
        # Set MLflow tracking URI
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        
        # Get model version from environment variable or auto-select latest
        import os
        requested_version = os.getenv("MODEL_VERSION", "auto")
        
        # Load the model
        logger.info(f"Loading model from MLflow (version: {requested_version})...")
        try:
            if requested_version == "auto" or requested_version == "latest":
                # Automatically get the highest version number
                client = mlflow.tracking.MlflowClient()
                versions = client.search_model_versions("name='fraud_detector'")
                if versions:
                    # Get the highest version number
                    latest_version = max([int(v.version) for v in versions])
                    model_uri = f"models:/fraud_detector/{latest_version}"
                    model = mlflow.sklearn.load_model(model_uri)
                    model_version = f"fraud_detector/v{latest_version}"
                    logger.info(f"✅ Model loaded: {model_version} (auto-selected highest version)")
                else:
                    raise Exception("No registered model versions found")
            else:
                # Load specific version
                model_uri = f"models:/fraud_detector/{requested_version}"
                model = mlflow.sklearn.load_model(model_uri)
                model_version = f"fraud_detector/v{requested_version}"
                logger.info(f"✅ Model loaded: {model_version}")
        except Exception as e:
            logger.warning(f"Could not load registered model: {e}")
            logger.info("Attempting to load from latest run...")
            # Fallback: load from latest run
            client = mlflow.tracking.MlflowClient()
            experiment = client.get_experiment_by_name("fraud_detection")
            if experiment:
                runs = client.search_runs(
                    experiment_ids=[experiment.experiment_id],
                    order_by=["start_time DESC"],
                    max_results=1
                )
                if runs:
                    run_id = runs[0].info.run_id
                    model_uri = f"runs:/{run_id}/model"
                    model = mlflow.sklearn.load_model(model_uri)
                    model_version = f"run/{run_id[:8]}"
                    logger.info(f"✅ Model loaded from run: {run_id}")
        
        # Initialize Feast feature store
        logger.info("Initializing Feast feature store...")
        feature_store = get_fraud_feature_store(repo_path="feature_store")
        logger.info("✅ Feature store initialized")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise


@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "message": "Fraud Detection API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "mlflow_connected": True,
        "feast_connected": feature_store is not None,
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_fraud(transaction: TransactionRequest):
    """Predict if a transaction is fraudulent"""
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare features in the correct order for the model
        features = np.array([[
            transaction.amt,
            transaction.city_pop,
            transaction.category_encoded,
            transaction.gender_encoded,
            transaction.state_encoded
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]  # Probability of fraud
        
        return PredictionResponse(
            trans_num=transaction.trans_num,
            is_fraud=bool(prediction),
            fraud_probability=float(probability),
            model_version=model_version or "unknown"
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/with-feast", response_model=PredictionResponse, tags=["Prediction"])
async def predict_fraud_with_feast(transaction: TransactionRequest):
    """Predict fraud using features from Feast online store"""
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if feature_store is None:
        raise HTTPException(status_code=503, detail="Feature store not initialized")
    
    try:
        # Get features from Feast online store
        entity_rows = [{
            "trans_num": transaction.trans_num
        }]
        
        try:
            online_features = feature_store.get_online_features(
                entity_rows=entity_rows,
                features=["fraud_detection_v1"]
            )
            
            # Extract feature values
            features_dict = online_features.to_dict()
            features = np.array([[
                features_dict.get('amt', [transaction.amt])[0],
                features_dict.get('city_pop', [transaction.city_pop])[0],
                features_dict.get('category_encoded', [transaction.category_encoded])[0],
                features_dict.get('gender_encoded', [transaction.gender_encoded])[0],
                features_dict.get('state_encoded', [transaction.state_encoded])[0]
            ]])
        except Exception as feast_error:
            logger.warning(f"Feast lookup failed: {feast_error}, using request data")
            # Fallback to request data
            features = np.array([[
                transaction.amt,
                transaction.city_pop,
                transaction.category_encoded,
                transaction.gender_encoded,
                transaction.state_encoded
            ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        
        return PredictionResponse(
            trans_num=transaction.trans_num,
            is_fraud=bool(prediction),
            fraud_probability=float(probability),
            model_version=model_version or "unknown"
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
