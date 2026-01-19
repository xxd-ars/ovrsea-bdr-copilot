#!/bin/bash

# Function to kill child processes when script exits
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $(jobs -p) > /dev/null 2>&1
    echo "✅ Shutdown complete."
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

echo "🚀 Starting OVRSEA BDR Tool..."
echo "=============================="

# 1. Start Backend (in background)
# PYTHONUNBUFFERED=1 forces realtime output, crucial for seeing agent thoughts
echo "🐍 Starting FastAPI Backend (Port 8000)..."
export PYTHONUNBUFFERED=1
(cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) &

# Wait a moment for backend to initialize
sleep 2

# 2. Start Frontend (in foreground)
echo "⚛️  Starting React Frontend (Port 5173)..."
echo "👉 View the logs below. Press Ctrl+C to stop both."
echo "=============================="
(cd frontend && npm run dev)

# Wait for any process to exit
wait