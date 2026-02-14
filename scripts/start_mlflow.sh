#!/bin/bash

# Start MLflow UI server
echo "Starting MLflow UI..."
echo "MLflow UI will be available at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --port 5001
