#!/bin/bash

# ADK Chatbot - Run Script
# This script sets up and runs the FastAPI chatbot application

set -e

echo "Starting ADK Chatbot..."

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Run the application
echo "Starting FastAPI server on http://localhost:8000"
python run.py
