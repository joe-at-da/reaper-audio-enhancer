# Getting Started - REAPER Audio Enhancement Tool

## Quick Overview

This tool helps you improve audio quality by:
- **Detecting and reducing background noise** from your audio
- **Analyzing video** to understand scene context
- **Suggesting ambient sounds** that match each scene
- **Creating REAPER tracks** with all suggestions ready to use

## Step-by-Step Guide

### 1. Launch the App

**Demo Mode** (with sample files pre-loaded):
```bash
bash launch.sh demo_snow    # Snowstorm video + audio
bash launch.sh demo_rain    # Rain video + audio
bash launch.sh demo_car     # Car video + audio
```

**Normal Mode** (select your own files):
```bash
bash launch.sh
```

Or use the GUI launcher if available.

### 2. Select Your Files

**Audio File (Required):**
- Click "Browse Audio"
- Select your audio file (WAV, MP3, FLAC, etc.)

**Video File (Optional but Recommended):**
- Click "Browse Video"
- Select your video file (MP4, MOV, AVI, etc.)
- The app will analyze scenes in your video

### 3. Analyze
- Click **"1. Analyze"**
- Wait for analysis to complete
- The app will:
  - Detect background noise
  - Analyze video scenes (if provided)
  - Generate audio suggestions for each scene

### 4. Process Audio (Optional)
- Adjust **"Noise Reduction Strength"** slider (0.0 = none, 1.0 = maximum)
- Click **"2. Process Audio"** to save noise-reduced audio
- This creates a standalone audio file you can use anywhere

### 5. Export to REAPER
- Click **"3. Export to REAPER"**
- The app will:
  - Generate a REAPER project file
  - Create audio tracks with suggestions
  - Install video import script
  - Show you next steps

### 6. Import to REAPER
- Click **"4. Import to REAPER"**
- REAPER will open with your project
- Video will be added automatically (if OSC is enabled) ✅

### 7. Add Video (Automatic or Manual)

**Option A: Automatic via OSC (Recommended)** ✅
- If you've set up OSC automation (see `OSC_AUTOMATION_SETUP.md`):
  - Video will be added automatically when REAPER opens
  - No manual steps required!

**Option B: Manual**
1. In REAPER: **Actions > Show action list**
2. Search for: **"Add Video to Project"**
3. Click **Run**
4. Video track will be created!

**Option C: Insert Media File**
1. In REAPER: **Insert > Media File**
2. Select your video file
3. Click **View > Video Window** (Cmd+Shift+V)
4. Click **Play**

### 8. View Your Project

- **Video Window**: View > Video Window (Cmd+Shift+V)
- **Audio Tracks**: Your original audio + suggested enhancement tracks
- **Play**: Click Play to hear your audio with video

## Settings

### Language
- Change between English and Ukrainian
- Affects all UI text and messages

### REAPER OSC Settings
- Configure connection to REAPER (advanced)
- Default: 127.0.0.1:9000

### VLC Player
- Automatically detected and configured
- Required for video playback in REAPER
- Download: https://www.videolan.org/vlc/

## Tips & Tricks

### Best Results
- Use clear audio files (WAV or FLAC preferred)
- Use video files that match your audio duration
- Adjust noise reduction strength to your preference

### Noise Reduction
- **0.0**: No noise reduction (original audio)
- **0.5**: Moderate noise reduction (recommended)
- **1.0**: Maximum noise reduction (may remove some audio detail)

### Scene Detection & Suggestions
- The app detects scenes in your video (e.g., rain, car, outdoor)
- For each scene, it suggests matching ambient sounds
- Each suggestion is on a separate REAPER track
- Mute or adjust volume of any track you don't want
- **Smart deduplication**: No duplicate suggestions for the same scene

### Exporting Your Work
- Use REAPER's export features to save your final mix
- All tracks are ready for further editing

## Troubleshooting

### Video Not Showing
- Make sure VLC is installed (Settings shows status)
- Close and restart REAPER after adding video
- Check that video file path is correct

### Audio Not Playing
- Verify audio file is valid (try in another player)
- Check REAPER's audio settings
- Make sure audio device is connected

### Script Won't Load
- Verify script file exists: `~/Library/Application Support/REAPER/Scripts/add_video_to_reaper.lua`
- Try restarting REAPER
- Check that REAPER has permission to access the file

## File Locations

**Sample Files:**
```
~/Projects/ihor-audio-main/reaper-audio-enhancement/assets/sample_files/
  - sample_video.mp4 (4K snowstorm video)
  - sample_audio.wav (extracted audio)
```

**REAPER Projects:**
```
~/.reaper_audio_enhancement/exports/
  - project_YYYYMMDD_HHMMSS.rpp
  - export_YYYYMMDD_HHMMSS.json
```

**Video Script:**
```
~/Library/Application Support/REAPER/Scripts/
  - add_video_to_reaper.lua
```

## Demo Modes

Test the tool with pre-loaded sample files:

```bash
bash launch.sh demo_snow   # Snowstorm video + audio
bash launch.sh demo_rain   # Rain video + audio
bash launch.sh demo_car    # Car video + audio
```

Each demo mode includes:
- Pre-selected video and audio files
- Matching audio suggestions
- Ready to analyze, process, and export

See `DEMO_MODES_SETUP.md` for details.

## OSC Automation Setup

Enable automatic video addition to REAPER projects:

1. Edit REAPER configuration file
2. Enable OSC in REAPER preferences
3. Restart REAPER

See `OSC_AUTOMATION_SETUP.md` for step-by-step instructions.

## Need Help?

See the other documentation files:
- `DEMO_MODES_SETUP.md` - Demo modes explained
- `OSC_AUTOMATION_SETUP.md` - Automatic video addition
- `SCENE_DETECTION_IMPROVEMENTS.md` - How scene detection works
- `VLC_SETUP.md` - VLC installation and configuration
- `FINAL_STATUS.md` - Complete technical details
- `FINAL_VIDEO_SOLUTION.md` - Video integration explained

## Summary

The tool is designed to be intuitive:
1. **Select files** → 2. **Analyze** → 3. **Process** → 4. **Export** → 5. **Import** → 6. **Add video** → 7. **Enjoy!**

That's it! Your audio is now enhanced with scene-matched suggestions and video.
