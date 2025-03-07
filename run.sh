#!/bin/bash

echo "=============================================="
echo "      Medical Diagnosis System Launcher"
echo "=============================================="

# Get the absolute path to the project root and models directory
PROJECT_ROOT=$(dirname "$(readlink -f "$0")")
MODELS_DIR="${PROJECT_ROOT}/models"

# Change to the codebase directory
cd "${PROJECT_ROOT}/codebase" || {
  echo "Error: Could not change to codebase directory."
  read -p "Press Enter to continue..."
  exit 1
}

# Check if models directory exists at project root
if [ ! -d "$MODELS_DIR" ]; then
  echo "Notice: Models directory not found at $MODELS_DIR"
  echo "Creating models directory at project root..."
  mkdir -p "$MODELS_DIR"
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
  echo "Error: Python is not installed. Please install Python 3 and try again."
  read -p "Press Enter to continue..."
  exit 1
fi

# Get the local IP address
IP_ADDRESS=$(hostname -I | awk '{print $1}')
if [ -z "$IP_ADDRESS" ]; then
  IP_ADDRESS="localhost"
fi

# Check if port 5000 is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t &> /dev/null; then
  echo "Warning: Port 5000 is already in use."
  echo "Attempting to close the application using port 5000..."
  
  PID=$(lsof -Pi :5000 -sTCP:LISTEN -t)
  if [ -n "$PID" ]; then
    echo "Killing process with PID $PID"
    kill -9 "$PID"
    if [ $? -eq 0 ]; then
      echo "Successfully closed the application."
    else
      echo "Failed to close the application. Please close it manually."
    fi
  fi
fi

# Start the server with the models directory path
echo "Starting server..."
export MODELS_PATH="$MODELS_DIR"
python3 server.py > server_log.txt 2>&1 &
SERVER_PID=$!

# Wait for the server to start and check its health
echo "Waiting for server to initialize..."
echo "This may take up to 8 seconds..."

SERVER_READY=0
for i in {1..5}; do
  sleep 1
  echo "Checking server health $i/5..."
  if curl -s http://localhost:5000/health &> /dev/null; then
    SERVER_READY=1
    echo "Server is ready!"
    break
  fi
done

if [ $SERVER_READY -eq 0 ]; then
  echo "Error: Server failed to start properly."
  echo "Checking server log for errors:"
  if [ -f server_log.txt ]; then
    cat server_log.txt
  else
    echo "No server log file found."
  fi
  read -p "Press Enter to continue..."
  exit 1
fi

echo "=============================================="
echo "Medical Diagnosis System is now running!"
echo "=============================================="
echo ""
echo "Access the web interface at:"
echo "  http://localhost:5000  (local access)"
echo "  http://$IP_ADDRESS:5000  (network access)"
echo ""
echo "Opening web browser..."
if command -v xdg-open &> /dev/null; then
  xdg-open http://localhost:5000
elif command -v open &> /dev/null; then
  open http://localhost:5000
else
  echo "Could not automatically open browser. Please open http://localhost:5000 manually."
fi

echo "Press Ctrl+C to exit and shutdown the server..."
wait $SERVER_PID

echo "Done."