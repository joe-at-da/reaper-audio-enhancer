# Demo Mode - Quick Onboarding Guide

## What is Demo Mode?

Demo Mode is a quick onboarding experience where the application **automatically loads sample audio and video files**. This allows you to immediately test the full workflow without having to browse for files.

**Perfect for**: First-time users, testing, demonstrations, and onboarding.

---

## How to Launch Demo Mode

### Option 1: Shell Script (Easiest)
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
bash launch.sh demo
```

### Option 2: Python with Demo Flag
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
source venv/bin/activate
python run.py --demo
```

### Option 3: Short Form
```bash
bash launch.sh -d
# or
python run.py -d
```

---

## What You'll See in Demo Mode

When you launch in demo mode, the application will:

1. **Pre-load Sample Audio**
   - File: `sample_audio.wav` (10 seconds with background noise)
   - Shows: "sample_audio.wav (Demo)"
   - Status: "Demo mode: Sample audio loaded"

2. **Pre-load Sample Video**
   - File: `sample_video.mp4` (10 seconds with scene transitions)
   - Shows: "sample_video.mp4 (Demo)"
   - Status: "Demo mode: Sample audio and video loaded - Ready to analyze!"

3. **Pre-set Noise Reduction**
   - Strength: 0.5 (moderate reduction)
   - Ready to use immediately

---

## Demo Mode Workflow

### Step 1: Launch Demo Mode
```bash
bash launch.sh demo
```

### Step 2: Application Opens
You'll see:
- Audio File: `sample_audio.wav (Demo)` ✓
- Video File: `sample_video.mp4 (Demo)` ✓
- Noise Reduction Strength: 0.5
- Status: "Demo mode: Sample audio and video loaded - Ready to analyze!"

### Step 3: Click "Analyze"
- Analyzes the sample audio for noise
- Analyzes the sample video for scenes
- Takes ~5 seconds
- Shows detected scenes and suggestions

### Step 4: Review Results
- See detected scene type (e.g., "storm", "outdoor")
- See confidence level
- See suggested audio enhancements

### Step 5: Choose Action

**Option A: Process Audio**
- Click "Process Audio"
- Saves processed audio as `processed_sample_audio.wav`
- Noise reduced by 50%

**Option B: Export to REAPER**
- Click "Export to REAPER"
- Generates JSON export file
- Creates separate audio/video/enhancement tracks
- Ready to import into REAPER

---

## What the Sample Files Contain

### sample_audio.wav
- **Duration**: 10 seconds
- **Content**: Sine wave (440 Hz tone) + background noise
- **Purpose**: Test noise detection and reduction
- **Noise Level**: Moderate (good for testing)

### sample_video.mp4
- **Duration**: 10 seconds
- **Content**: Scene transitions (clear sky → storm)
- **Colors**: Blue (clear) → Dark (storm)
- **Purpose**: Test scene detection
- **Scenes**: Transitions from "quiet" → "storm"

---

## Demo Mode Use Cases

### Use Case 1: First-Time User
**Goal**: Understand how the tool works

**Steps**:
1. Launch: `bash launch.sh demo`
2. Click "Analyze"
3. Review results
4. Click "Process Audio"
5. See the processed file created

**Time**: ~2 minutes

### Use Case 2: Testing New Features
**Goal**: Verify functionality works

**Steps**:
1. Launch: `bash launch.sh demo`
2. Adjust noise reduction slider
3. Click "Analyze"
4. Try different settings
5. Export to REAPER

**Time**: ~5 minutes

### Use Case 3: Live Demonstration
**Goal**: Show someone how the tool works

**Steps**:
1. Launch: `bash launch.sh demo`
2. Explain the interface
3. Click "Analyze" to show detection
4. Show suggestions
5. Export to REAPER

**Time**: ~10 minutes

### Use Case 4: Onboarding New Users
**Goal**: Get users started quickly

**Steps**:
1. Provide command: `bash launch.sh demo`
2. Let them explore
3. Have them try "Analyze"
4. Have them try "Process Audio"
5. Have them try "Export to REAPER"

**Time**: ~15 minutes

---

## Switching Between Modes

### Normal Mode (Browse for Files)
```bash
bash launch.sh
# or
python run.py
```

### Demo Mode (Pre-loaded Files)
```bash
bash launch.sh demo
# or
python run.py --demo
```

You can switch between modes by relaunching with different commands.

---

## Demo Mode Features

### ✓ What Works
- Audio analysis with sample file
- Video scene detection with sample file
- Noise reduction processing
- Audio export functionality
- REAPER export generation
- All three buttons (Analyze, Process Audio, Export to REAPER)

### ✓ What's Pre-loaded
- Sample audio file
- Sample video file
- Noise reduction strength (0.5)
- Status messages

### ✓ What You Can Still Do
- Adjust noise reduction strength slider
- Browse for different audio files
- Browse for different video files
- Run analysis
- Process audio
- Export to REAPER

---

## Customizing Demo Mode

### Use Your Own Sample Files

If you want to use different sample files, you can:

1. **Replace the sample files**:
   - Replace `assets/sample_files/sample_audio.wav`
   - Replace `assets/sample_files/sample_video.mp4`

2. **Or browse for different files**:
   - Click "Browse Audio" to select different audio
   - Click "Browse Video" to select different video
   - Demo mode just pre-loads the defaults

---

## Troubleshooting Demo Mode

### Issue: Demo mode doesn't load files
**Solution**: Check that sample files exist
```bash
ls assets/sample_files/
# Should show: sample_audio.wav, sample_video.mp4
```

### Issue: Files show as "No file selected"
**Solution**: Restart the application
```bash
bash launch.sh demo
```

### Issue: Want to switch to normal mode
**Solution**: Launch without demo flag
```bash
bash launch.sh
# or
python run.py
```

---

## Demo Mode Status Messages

| Message | Meaning |
|---------|---------|
| "Demo mode: Sample audio loaded" | Audio file pre-loaded |
| "Demo mode: Sample audio and video loaded - Ready to analyze!" | Both files pre-loaded, ready to go |
| "Analysis complete" | Analysis finished, results available |
| "Audio processed: processed_sample_audio.wav" | Processing complete |
| "Exported: export_YYYYMMDD_HHMMSS.json" | Export complete |

---

## Quick Reference

| Task | Command |
|------|---------|
| Launch demo mode | `bash launch.sh demo` |
| Launch normal mode | `bash launch.sh` |
| Demo with Python | `python run.py --demo` |
| Normal with Python | `python run.py` |
| Check sample files | `ls assets/sample_files/` |

---

## Next Steps

1. **Try Demo Mode**
   ```bash
   bash launch.sh demo
   ```

2. **Click "Analyze"**
   - See noise detection
   - See scene detection
   - Review suggestions

3. **Try "Process Audio"**
   - See processed file created
   - Check the output

4. **Try "Export to REAPER"**
   - See export file created
   - Review the JSON format

5. **Read the User Guide**
   - See `USER_GUIDE.md` for detailed instructions
   - See `QUICKSTART.md` for workflow examples

---

## Summary

Demo Mode provides a **quick, guided onboarding experience** with:
- ✓ Pre-loaded sample files
- ✓ No need to browse for files
- ✓ Ready-to-use settings
- ✓ Full functionality testing
- ✓ Perfect for first-time users

**Launch with**: `bash launch.sh demo`

---

**Happy exploring!**
