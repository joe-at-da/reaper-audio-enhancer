# Export vs Import - Clear Explanation

---

## The Simple Version

### **EXPORT TO REAPER** Button
**What it does**: Saves your analysis results to a JSON file

**When to click it**: After you've analyzed audio/video

**What happens**:
1. Analysis results are saved to: `~/.reaper_audio_enhancement/exports/export_YYYYMMDD_HHMMSS.json`
2. Success dialog shows the file path
3. That's it - the file is ready to use

**What the file contains**:
- Your audio file path
- Your video file path (if provided)
- Noise reduction strength setting
- Suggested audio files for each scene
- Timing information for each suggestion

---

### **IMPORT TO REAPER** Button
**What it does**: Takes the JSON file and creates tracks in REAPER automatically

**When to click it**: After you've exported and want to use the results in REAPER

**What happens**:
1. File browser opens - you select the JSON file
2. Application validates the file
3. **Option A - OSC Method** (if REAPER is running):
   - Automatically creates tracks in REAPER
   - Original Audio track
   - Video track (if provided)
   - Enhancement tracks with suggested audio
   - All with correct timing, volume, and fades
   - Done! Tracks appear in REAPER
4. **Option B - ReaScript Method** (if REAPER not running):
   - Generates a Python script file
   - Shows instructions on how to run it in REAPER
   - You run the script in REAPER's Script Editor
   - Tracks are created

---

## The Complete Workflow

### **Step 1: Analyze**
```
1. Select audio file
2. Select video file (optional)
3. Click "Analyze"
4. Wait for analysis to complete
```

### **Step 2: Export**
```
1. Click "Export to REAPER"
2. Dialog shows success and file path
3. JSON file is saved
```

### **Step 3: Import**
```
1. Click "Import to REAPER"
2. Select the JSON file from step 2
3. REAPER creates tracks automatically (or generates script)
```

---

## What You DON'T Need to Do

❌ Don't manually add audio files to REAPER  
❌ Don't manually set timing for each track  
❌ Don't manually set volume for each track  
❌ Don't manually add fades  
❌ Don't edit the JSON file  
❌ Don't run command-line tools (unless you want to)  

---

## What The Tool DOES For You

✓ Analyzes audio for noise  
✓ Detects scenes in video  
✓ Suggests ambient sounds for each scene  
✓ Exports all this as JSON  
✓ **Automatically creates REAPER tracks** with:
  - Correct audio files
  - Correct timing
  - Correct volume
  - Correct fades
  - Correct effects

---

## Example Workflow

### **Scenario: You have a video with background noise**

**Step 1: Analyze**
- Select your audio file
- Select your video file
- Click "Analyze"
- Tool detects: "outdoor scene with traffic noise"
- Tool suggests: "add bird sounds, reduce traffic"

**Step 2: Export**
- Click "Export to REAPER"
- JSON file saved with all suggestions

**Step 3: Import**
- Click "Import to REAPER"
- Select the JSON file
- REAPER automatically creates:
  - "Original Audio" track with your audio
  - "Video" track with your video
  - "Enhancement - outdoor" track with bird sounds
  - All positioned correctly with proper timing

**Step 4: Edit in REAPER**
- Adjust volume if needed
- Add effects if needed
- Export final mix

---

## Settings (Optional)

### **Why Configure REAPER Settings?**

The tool tries to connect to REAPER automatically using:
- **Host**: 127.0.0.1 (your computer)
- **Port**: 9000 (REAPER's default)

**You only need to change these if**:
- REAPER is on a different computer (change Host)
- REAPER uses a different port (change Port)

**How to configure**:
1. Click Settings
2. Go to "REAPER OSC Settings"
3. Enter your REAPER's IP and port
4. Click OK

**If you don't configure**:
- Tool uses defaults (127.0.0.1:9000)
- Works fine for most users
- Falls back to ReaScript if OSC fails

---

## Two Import Methods

### **Method 1: OSC (Automatic)**
- **When**: REAPER is running
- **What happens**: Tracks created instantly in REAPER
- **User action**: None - automatic!
- **Best for**: Quick workflow

### **Method 2: ReaScript (Manual)**
- **When**: REAPER not running or OSC fails
- **What happens**: Script file generated
- **User action**: Run script in REAPER's Script Editor
- **Best for**: Offline work, batch processing

---

## Troubleshooting

### **Import fails with "Audio file not found"**
- The JSON references audio files that don't exist
- Make sure audio files are in the same location as when you exported

### **OSC connection fails**
- REAPER not running
- OSC not enabled in REAPER (Options > Preferences > Control/OSC/web)
- Different IP/port configured
- Solution: Use ReaScript method instead

### **ReaScript method shows instructions**
- This is normal
- Follow the instructions to run script in REAPER
- Script will create all tracks

---

## Summary

**EXPORT**: Saves analysis to JSON file  
**IMPORT**: Creates REAPER tracks from JSON file  

That's it! The tool handles all the complexity of:
- Organizing tracks
- Setting timing
- Setting volume
- Adding fades
- Configuring effects

You just click Export, then Import, and REAPER has all your tracks ready to edit!

---

## Quick Reference

| Action | Button | Result |
|--------|--------|--------|
| **Analyze** | Analyze | Detects noise and scenes |
| **Export** | Export to REAPER | Saves JSON file |
| **Import** | Import to REAPER | Creates REAPER tracks |
| **Configure** | Settings | Set REAPER IP/port |

---

**That's all you need to know!**
