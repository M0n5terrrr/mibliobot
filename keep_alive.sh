#!/bin/bash

SCRIPT_NAME="main.py"
PYTHON_EXECUTABLE="python3" # Or "python" depending on your system

while true; do
  if pgrep -f "$PYTHON_EXECUTABLE $SCRIPT_NAME"; then
    echo "$(date) - Bot is running."
  else
    echo "$(date) - Bot is NOT running. Restarting..."
    nohup $PYTHON_EXECUTABLE $SCRIPT_NAME &
  fi
  sleep 60 # Check every 60 seconds
done
