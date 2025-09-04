#!/bin/bash

echo "Deleting homes.db......"
if [ -f "homes.db" ]; then
    rm -rf homes.db
else
    echo "homes.db not found."
fi

# MarketMap Backend Server Run Script
echo "Starting MarketMap Backend Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run 'python3 -m venv venv' and 'pip install -r requirements.txt' first."
    exit 1
fi

# Activate virtual environment - use . instead of source for better compatibility
echo "Activating virtual environment..."
. venv/bin/activate

# Check if required packages are installed
if ! python -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "Error: Required packages not found!"
    echo "Please run 'pip install -r requirements.txt' first."
    exit 1
fi

# Start the server
echo "Starting FastAPI server with uvicorn..."
echo "Server will be available at: http://localhost:8080"
echo "API documentation at: http://localhost:8080/docs"
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
