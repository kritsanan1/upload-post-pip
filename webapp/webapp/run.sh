#!/bin/bash

# Run script for Upload-Post AI WebApp

echo "Starting Upload-Post AI WebApp..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Install requirements if they don't exist
if [ ! -f "requirements_installed" ]; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    touch requirements_installed
    echo "Requirements installed successfully!"
fi

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Please configure your API keys."
fi

# Start the Flask application
echo "Starting Flask application..."
echo "WebApp will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py