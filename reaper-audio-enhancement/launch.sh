#!/bin/bash

# REAPER Audio Enhancement - Application Launcher
# Usage:
#   bash launch.sh              # Normal mode
#   bash launch.sh demo         # Demo mode (snowstorm)
#   bash launch.sh demo_snow    # Demo mode (snowstorm)
#   bash launch.sh demo_rain    # Demo mode (rain)
#   bash launch.sh demo_car     # Demo mode (car)

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Run the application
cd "$PROJECT_ROOT"

case "$1" in
    demo|demo_snow|-d|--demo)
        python run.py --demo snow
        ;;
    demo_rain)
        python run.py --demo rain
        ;;
    demo_car)
        python run.py --demo car
        ;;
    *)
        python run.py
        ;;
esac
