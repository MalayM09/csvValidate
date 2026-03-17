#!/bin/bash

# setup.sh - Environment Setup for Collaborators

echo "🚀 Starting environment setup for Google Sheet Validator..."

# 1. Check for Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# 2. Check for Node/NPM
if ! command -v npm &> /dev/null
then
    echo "❌ NPM not found. Please install Node.js."
    exit 1
fi

# 3. Backend Setup
echo "📦 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Frontend Setup
echo "📦 Installing frontend dependencies..."
cd client
npm install
cd ..

echo "✅ Setup complete!"
echo "👉 To start the tool, run: ./run.sh"
chmod +x run.sh
