#!/bin/bash

# REAPER Audio Enhancement - Application Launcher
# Usage:
#   bash launch.sh          # Normal mode
#   bash launch.sh demo     # Demo mode with sample files pre-loaded

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Run the application
cd "$PROJECT_ROOT"

if [ "$1" = "demo" ] || [ "$1" = "-d" ] || [ "$1" = "--demo" ]; then
    python run.py --demo
else
    python run.py
fi
