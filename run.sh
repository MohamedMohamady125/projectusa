#!/bin/bash

# SwimUSA Recruit Backend Startup Script

echo "🏊 Starting SwimUSA Recruit Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/bin/uvicorn" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create one from .env.example"
    echo "   cp .env.example .env"
    echo "   Then edit .env with your configuration"
    exit 1
fi

# Start the application
echo ""
echo "🚀 Starting FastAPI application..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/api/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
