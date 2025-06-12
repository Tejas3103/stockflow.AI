#!/bin/bash

# StockFlow.AI - Start Script
# This script starts both the backend and frontend services

echo "🚀 Starting StockFlow.AI..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please copy env.example to .env and configure your API keys:"
    echo "   cp env.example .env"
    echo "   # Then edit .env with your actual API keys"
    echo ""
fi

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting backend server..."
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ StockFlow.AI is starting up!"
echo "📊 Backend API: http://localhost:8000"
echo "🎨 Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for both processes
wait 