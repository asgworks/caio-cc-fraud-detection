# Credit Card Fraud Detection

A machine learning system for detecting fraudulent credit card transactions with support for both batch and real-time inference.

## Project Structure

```
.
├── data/                    # Data storage
│   ├── raw/                 # Original, immutable data
│   ├── processed/           # Cleaned, transformed data
│   ├── external/            # External data sources
│   └── streaming/           # Real-time data buffer
│
├── notebooks/               # Jupyter notebooks for exploration
│
├── src/                     # Source code
│   ├── data/                # Data processing
│   │   ├── batch/           # Batch processing
│   │   └── streaming/       # Streaming processing
│   ├── features/            # Feature engineering
│   ├── models/              # Model training and inference
│   ├── api/                 # REST API for real-time inference
│   └── utils/               # Utilities
│
├── models/                  # Saved model artifacts
├── tests/                   # Tests
├── configs/                 # Configuration files
├── scripts/                 # Executable scripts
└── docs/                    # Documentation

```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Usage

### Batch Processing
Train a model on historical data:
```bash
python scripts/batch/train_model.py
```

### Real-time API
Start the fraud detection API:
```bash
python scripts/streaming/start_api.py
```

### Streaming Consumer
Start the event consumer:
```bash
python scripts/streaming/start_consumer.py
```

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black src/ tests/
```

## Docker

Build and run with Docker:
```bash
docker-compose up --build
```
