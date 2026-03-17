#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

trap cleanup SIGINT

echo "Starting Google Sheet Validator Services..."

# Start Backend
source venv/bin/activate
python api.py &
BACKEND_PID=$!
echo "Backend started on http://localhost:8000 (PID: $BACKEND_PID)"

# Start Frontend
cd client
npm run dev &
FRONTEND_PID=$!
echo "Frontend starting... (PID: $FRONTEND_PID)"

echo "Services are running. Press Ctrl+C to stop."
wait
