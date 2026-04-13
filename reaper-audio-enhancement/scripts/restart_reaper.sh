#!/bin/bash
# Restart REAPER to pick up new VLC configuration

echo "Closing REAPER..."
pkill -f "REAPER" || true
sleep 2

echo "Restarting REAPER..."
open -a REAPER

echo "REAPER restarted. VLC configuration should now be active."
