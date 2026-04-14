# OSC Automation Setup - Automatic Video Addition

Enable automatic video addition to REAPER projects via OSC (Open Sound Control).

## What is OSC Automation?

When you export a project to REAPER, the app now automatically sends an OSC command to add the video track. No manual steps required!

**Before**: Export → REAPER opens → Manually run "add_video_to_reaper" action
**After**: Export → REAPER opens → Video added automatically ✅

---

## Setup Instructions

### Step 1: Register Custom Action in REAPER

Edit the REAPER configuration file:
```
~/Library/Application Support/REAPER/reaper-kb.ini
```

Add this line (if file is empty, just add this):
```
SCR 4 0 _ADD_VIDEO_TO_REAPER "Add Video to Project" "add_video_to_reaper.lua"
```

**What this does**:
- `SCR 4 0` - Defines a script action
- `_ADD_VIDEO_TO_REAPER` - Command ID (used by OSC)
- `"Add Video to Project"` - Display name in REAPER
- `"add_video_to_reaper.lua"` - Script file to run

### Step 2: Enable OSC in REAPER

1. **Open REAPER**
2. **Preferences** (Cmd+, on macOS)
3. Navigate to: **Control/OSC/web**
4. Click **Add** to add new OSC control surface
5. Select **OSC (Open Sound Control)**
6. Select **Local port mode**
7. Note the **Local listen port** (default: 9000)
8. Click **OK**

**Important**: The app sends OSC messages to `localhost:9000` by default.

### Step 3: Restart REAPER

After editing `reaper-kb.ini`, restart REAPER for changes to take effect.

### Step 4: Verify Setup

1. In REAPER: **Actions > Show action list**
2. Search for: **"Add Video to Project"**
3. You should see it in the list
4. Click **Run** to test it manually

If you see the action, OSC automation is ready!

---

## How It Works

### When You Export to REAPER

1. **App exports project** to REAPER format (.rpp)
2. **App opens REAPER** with the project file
3. **App waits 3 seconds** for REAPER to load
4. **App sends OSC message**: `/action/_ADD_VIDEO_TO_REAPER`
5. **REAPER receives message** and runs the script
6. **Video added automatically** ✅

### OSC Message Format

```
/action/_ADD_VIDEO_TO_REAPER
```

Sent to: `127.0.0.1:9000` (localhost, port 9000)

---

## Troubleshooting

### Video Not Added Automatically?

**Check 1: Is OSC enabled in REAPER?**
- Preferences > Control/OSC/web
- Should have an OSC control surface listed
- Port should be 9000

**Check 2: Is custom action registered?**
- Edit: `~/Library/Application Support/REAPER/reaper-kb.ini`
- Should contain: `SCR 4 0 _ADD_VIDEO_TO_REAPER "Add Video to Project" "add_video_to_reaper.lua"`
- Restart REAPER after editing

**Check 3: Check app logs**
- Look for: "OSC message sent: /action/_ADD_VIDEO_TO_REAPER"
- If not present, OSC client didn't send message

**Check 4: Is REAPER running?**
- App can only send OSC if REAPER is running
- If REAPER crashes, OSC message is lost

### Manual Fallback

If OSC automation doesn't work, you can still add video manually:

1. In REAPER: **Actions > Show action list**
2. Search for: **"Add Video to Project"**
3. Click **Run**
4. Video added manually

---

## Advanced Configuration

### Change OSC Port

If you use a different OSC port in REAPER:

Edit `src/gui/main_window.py`, line ~501:
```python
osc_client = get_osc_client(host="127.0.0.1", port=YOUR_PORT)
```

### Disable OSC Automation

If you prefer manual video addition:

Comment out line ~501 in `src/gui/main_window.py`:
```python
# osc_client.send_add_video_command(wait_ms=3000)
```

---

## Technical Details

### OSC Client Implementation

File: `src/utils/osc_client.py`

Features:
- Sends UDP OSC messages to REAPER
- Automatic retry with configurable delay
- Logging for debugging
- Cross-platform (macOS, Windows, Linux)

### Integration Point

File: `src/gui/main_window.py`, method `_open_reaper_with_project()`

When project is exported:
1. REAPER opens with project
2. OSC client sends add_video command
3. 3-second delay allows REAPER to load
4. Video script runs automatically

---

## FAQ

**Q: Does this work on Windows/Linux?**
A: Yes! OSC is platform-independent. Same setup on all platforms.

**Q: What if REAPER is already running?**
A: The app opens the project in the running instance. OSC still works.

**Q: Can I customize the delay?**
A: Yes, edit line ~501 in `src/gui/main_window.py`:
```python
osc_client.send_add_video_command(wait_ms=5000)  # 5 seconds instead of 3
```

**Q: What if OSC fails?**
A: The app logs a warning but continues. You can still add video manually.

---

## Summary

✅ **OSC automation enabled**
- Automatic video addition via OSC
- No manual steps required
- Fallback to manual if needed
- Cross-platform support

**Next**: Test with demo modes (demo_snow, demo_rain, demo_car)
