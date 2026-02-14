#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Activate caioenv virtual environment
echo "Activating caioenv environment..."
source "$PROJECT_DIR/caioenv/bin/activate"

# Set model version (default: latest, or pass as argument: ./start_api.sh 2)
MODEL_VERSION=${1:-latest}
export MODEL_VERSION

# Start the API server
echo "Starting Fraud Detection API..."
echo "Model Version: $MODEL_VERSION (auto = highest version number)"
echo "API will be available at: http://localhost:8000"
echo "API docs will be available at: http://localhost:8000/docs"
echo ""
echo "To load a different version: ./start_api.sh <version_number>"
echo "Example: ./start_api.sh 1"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$PROJECT_DIR"
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
