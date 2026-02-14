#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Activate caioenv virtual environment
echo "Activating caioenv environment..."
source "$PROJECT_DIR/caioenv/bin/activate"

# Start MLflow UI server
echo "Starting MLflow UI..."
echo "MLflow UI will be available at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$PROJECT_DIR"
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --port 5001
