# Video Automation Research - OSC Solution

## Problem
Currently, video must be added manually to REAPER after export:
1. User exports project from app
2. REAPER opens with audio tracks
3. User must manually: Actions > Show action list > search "add_video_to_reaper" > Run

## Solution: OSC (Open Sound Control)
REAPER supports triggering custom actions via OSC messages from external applications.

### How It Works
1. **App sends OSC message** to REAPER (localhost:9000)
2. **REAPER receives** `/action/_ADD_VIDEO_TO_REAPER` message
3. **REAPER executes** the video import script automatically
4. **Video added** to project without user interaction

### Implementation Steps

#### Step 1: Register Custom Action in REAPER
Edit `~/Library/Application Support/REAPER/reaper-kb.ini` and add:
```
SCR 4 0 _ADD_VIDEO_TO_REAPER "Add Video to Project" "add_video_to_reaper.lua"
```

#### Step 2: Enable OSC in REAPER
1. Preferences > Control/OSC/web
2. Add new OSC control surface
3. Select "Local port mode"
4. Note the listen port (default: 9000)

#### Step 3: Send OSC from Python App
```python
import socket

def send_osc_command(command, host="127.0.0.1", port=9000):
    """Send OSC message to REAPER"""
    # OSC message format: /action/_COMMAND_ID
    message = f"/action/{command}".encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (host, port))
    sock.close()

# Trigger video import
send_osc_command("_ADD_VIDEO_TO_REAPER")
```

#### Step 4: Call from App After Export
In `main_window.py`, after generating REAPER project:
```python
# Open REAPER with project
self._open_reaper_with_project(str(project_path))

# Wait for REAPER to load (2 seconds)
time.sleep(2)

# Send OSC command to add video
send_osc_command("_ADD_VIDEO_TO_REAPER")
```

### Advantages
✅ No user interaction required
✅ Works across platforms (macOS, Windows, Linux)
✅ Uses official REAPER API
✅ Reliable and tested approach
✅ Can trigger any REAPER action via OSC

### Limitations
⚠️ Requires REAPER to be running
⚠️ Requires OSC to be enabled in REAPER preferences
⚠️ Timing: May need delay for REAPER to load project

### Alternative: Command-Line Parameters
REAPER supports command-line parameters:
```bash
reaper.exe -script "path/to/script.lua" project.rpp
```
However, this is less reliable than OSC for post-load actions.

### Alternative: Lua Deferred Scripts
Use `__startup.lua` with deferred execution:
- ✅ Runs automatically on startup
- ❌ Runs for ALL projects (not just ours)
- ❌ Can't distinguish our projects from user's

### Recommendation
**Use OSC method** - Most reliable, flexible, and doesn't interfere with user's normal REAPER usage.

---

## Implementation Checklist

- [ ] Add OSC helper function to `src/utils/osc_client.py`
- [ ] Update `main_window.py` to send OSC after export
- [ ] Register custom action in `reaper-kb.ini`
- [ ] Test with snowstorm video
- [ ] Test with rain video
- [ ] Test with car video
- [ ] Document in Getting Started guide
- [ ] Add error handling for REAPER not running

---

## Sample Videos Needed

### Rain Video
- Source: Pexels, Pixabay, Unsplash
- Duration: 10-15 seconds
- Content: Clear rain scene (outdoor or window view)
- File: `assets/sample_files/sample_video_rain.mp4`

### Car Video
- Source: Pexels, Pixabay, Unsplash
- Duration: 10-15 seconds
- Content: Driving/car interior
- File: `assets/sample_files/sample_video_car.mp4`

### Snow Video (Already Have)
- File: `assets/sample_files/sample_video.mp4`

---

## Demo Modes

After videos are in place:
```bash
bash launch.sh demo_snow   # Current snowstorm video
bash launch.sh demo_rain   # Rain video + rain audio suggestions
bash launch.sh demo_car    # Car video + car audio suggestions
```

Each demo mode loads appropriate video and audio suggestions.
