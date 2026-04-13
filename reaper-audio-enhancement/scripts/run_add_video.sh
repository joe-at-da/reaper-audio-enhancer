#!/bin/bash
# Simple script to run the add_video_to_reaper.py script in REAPER

SCRIPT_PATH="$HOME/Library/Application Support/REAPER/Scripts/add_video_to_reaper.py"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Video script not found at $SCRIPT_PATH"
    exit 1
fi

echo "Running video import script in REAPER..."
echo "Script path: $SCRIPT_PATH"

# Open REAPER with the script
open -a REAPER --args "--script=$SCRIPT_PATH"

echo "Done! Check REAPER for the video track."
