# Model Serving API

## Overview

FastAPI-based REST API for real-time fraud detection predictions using:
- **MLflow** - Load and serve trained models
- **Feast** - Feature retrieval from online store (optional)
- **FastAPI** - High-performance async API framework

## Quick Start

```bash
# Start the API server
bash scripts/start_api.sh
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## API Endpoints

### 1. Health Check
```bash
GET /health
```

Returns API health status and component availability.

### 2. Predict (Direct)
```bash
POST /predict
```

Make fraud predictions using features from the request body.

**Request Body**:
```json
{
  "trans_num": "txn_12345",
  "cc_num": "1234567890123456",
  "merchant": "Amazon",
  "amt": 49.99,
  "city_pop": 50000,
  "category_encoded": 8,
  "gender_encoded": 1,
  "state_encoded": 5
}
```

**Response**:
```json
{
  "trans_num": "txn_12345",
  "is_fraud": false,
  "fraud_probability": 0.02,
  "model_version": "fraud_detector/latest"
}
```

### 3. Predict with Feast
```bash
POST /predict/with-feast
```

Make fraud predictions using features from Feast online store (falls back to request data if not found).

## Example Usage

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "trans_num": "txn_001",
    "cc_num": "1234567890123456",
    "merchant": "Amazon",
    "amt": 49.99,
    "city_pop": 50000,
    "category_encoded": 8,
    "gender_encoded": 1,
    "state_encoded": 5
  }'
```

### Using Python
```python
import requests

# Predict endpoint
url = "http://localhost:8000/predict"
data = {
    "trans_num": "txn_001",
    "cc_num": "1234567890123456",
    "merchant": "Amazon",
    "amt": 49.99,
    "city_pop": 50000,
    "category_encoded": 8,
    "gender_encoded": 1,
    "state_encoded": 5
}

response = requests.post(url, json=data)
print(response.json())
```

## Architecture

```
Request → FastAPI → MLflow (Load Model) → Prediction
                  ↓
                Feast (Optional: Get Features)
```

1. **Startup**: API loads the latest model from MLflow registry
2. **Request**: Client sends transaction data
3. **Feature Retrieval** (optional): Get features from Feast online store
4. **Prediction**: Model makes fraud prediction
5. **Response**: Return fraud probability and classification

## Configuration

The API automatically:
- Loads the latest registered model from MLflow (`models:/fraud_detector/latest`)
- Falls back to the most recent run if no registered model exists
- Initializes Feast feature store from `feature_store/`
- Serves on port 8000 with auto-reload in development

## Deployment

For production deployment:
1. Remove `--reload` flag from `start_api.sh`
2. Use a production ASGI server like Gunicorn:
   ```bash
   gunicorn src.api.app:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
3. Set up proper authentication and rate limiting
4. Use HTTPS with SSL certificates
5. Deploy behind a reverse proxy (nginx, traefik)

## Monitoring

Check API metrics at:
- `/health` - Component health status
- `/docs` - Interactive API documentation
- MLflow UI - Model performance tracking
- Application logs - Prediction requests and errors
