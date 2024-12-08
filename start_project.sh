#!/bin/bash

# Function to check if a port is in use and terminate the process
kill_if_port_in_use() {
  local PORT=$1
  if lsof -i :$PORT >/dev/null; then
    echo "Port $PORT is in use. Terminating the process..."
    PID=$(lsof -t -i :$PORT) # Get process ID
    kill -9 $PID # Terminate process
    echo "Process on port $PORT has been terminASGIated."
  else
    echo "Port $PORT is free."
  fi
}

# Function to check and fix permissions for a directory or file
check_and_fix_permissions() {
  local TARGET=$1
  if [ ! -e "$TARGET" ]; then
    echo "Target $TARGET does not exist. Creating it..."
    mkdir -p "$TARGET"
  fi
  if [ ! -r "$TARGET" ] || [ ! -w "$TARGET" ]; then
    echo "Permissions for $TARGET are not correct. Setting permissions..."
    chmod +rw "$TARGET"
    if [ $? -ne 0 ]; then
      echo "Error setting permissions for $TARGET. Exiting script."
      exit 1
    fi
  else
    echo "Permissions for $TARGET are correct."
  fi
}

# Paths to required directories
BACKEND_DIR="./app"
FRONTEND_DIR="./frontend"
FILES_DIR="./data"

# Check and fix permissions for important directories
check_and_fix_permissions "$BACKEND_DIR"
check_and_fix_permissions "$FRONTEND_DIR"
check_and_fix_permissions "$FILES_DIR"

# Check backend port and terminate process if necessary
BACKEND_PORT=8000
kill_if_port_in_use $BACKEND_PORT

# Start backend with hot-reload
echo "Starting backend with hot-reload on port $BACKEND_PORT..."
# cd $BACKEND_DIR || exit 1
if [ ! -d ".venv" ]; then
  echo "Virtual environment (.venv) not found. Creating it..."
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload &
BACKEND_PID=$!

# Check frontend port and terminate process if necessary
FRONTEND_PORT=3000
kill_if_port_in_use $FRONTEND_PORT

# Start frontend with hot-reload
echo "Starting frontend..."
cd $FRONTEND_DIR || exit 1
npm install
npm run dev &
FRONTEND_PID=$!

# Catch CTRL+C and terminate backend and frontend
trap "kill $BACKEND_PID $FRONTEND_PID" INT

# Wait for processes
wait
