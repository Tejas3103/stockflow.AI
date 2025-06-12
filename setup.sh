#!/bin/bash

# StockFlow.AI - Setup Script
# This script sets up the entire project for new users

echo "🚀 Setting up StockFlow.AI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Set up environment variables
if [ ! -f ".env" ]; then
    echo "📝 Setting up environment variables..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from env.example"
        echo "⚠️  IMPORTANT: Please edit .env file with your actual API keys!"
        echo "   Required keys: OPENAI_API_KEY, TAVILY_API_KEY"
    else
        echo "⚠️  env.example not found. Please create .env file manually."
    fi
else
    echo "✅ .env file already exists"
fi

# Install frontend dependencies
echo "🎨 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Make start script executable
chmod +x start.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run the application:"
echo "   Linux/Mac: ./start.sh"
echo "   Windows: start.bat"
echo ""
echo "Or run manually:"
echo "  Terminal 1: cd backend && python -m uvicorn main:app --reload"
echo "  Terminal 2: cd frontend && npm run dev"
echo "" 