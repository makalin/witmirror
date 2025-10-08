#!/bin/bash

# WitMirror Setup Script
echo "🪞 Setting up WitMirror..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd api
pip install -r requirements.txt
cd ..

# Create environment file if it doesn't exist
if [ ! -f "api/.env" ]; then
    echo "📝 Creating environment file..."
    cp api/env.example api/.env
    echo "⚠️  Please edit api/.env and add your OpenAI API key (optional)"
fi

# Create database directory
mkdir -p api/data

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the development servers:"
echo "  Frontend: npm run dev"
echo "  Backend:  cd api && uvicorn main:app --reload"
echo ""
echo "🌐 The app will be available at:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
