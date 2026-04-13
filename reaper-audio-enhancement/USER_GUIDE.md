# REAPER Audio Enhancement Tool - User Guide

## What This Tool Does

The REAPER Audio Enhancement Tool is designed to improve your audio quality by intelligently detecting and reducing noise while suggesting contextual audio enhancements based on video content.

### Main Features

1. **Noise Detection & Reduction**
   - Analyzes your audio to identify background noise
   - Applies spectral subtraction to reduce noise
   - Preserves important audio content while removing unwanted noise

2. **Video Scene Detection**
   - Analyzes video to understand the context (storm, car ride, outdoor, indoor, etc.)
   - Helps determine what audio enhancements would be appropriate
   - Provides confidence scores for detected scenes

3. **Audio Suggestions**
   - Recommends contextual ambient sounds based on detected video scenes
   - Includes a library of pre-recorded ambient sounds (wind, rain, thunder, etc.)
   - Suggests volume and fade settings for natural blending

4. **Track Organization**
   - Creates separate audio and video tracks in REAPER
   - Maintains original audio alongside processed versions
   - Allows easy A/B comparison and adjustment

---

## How to Use

### Step 1: Load Your Files

**Audio File (Required)**
- Click "Browse Audio" button
- Select your audio file (WAV, MP3, or FLAC format)
- The filename will appear next to the button

**Video File (Optional)**
- Click "Browse Video" button
- Select your video file (MP4, MOV, or AVI format)
- Video is used for scene detection to provide better suggestions
- If no video is selected, the tool will still work with audio only

### Step 2: Adjust Settings

**Noise Reduction Strength**
- Use the slider to set how aggressively to reduce noise
- **0.0** = No noise reduction (original audio)
- **0.5** = Moderate noise reduction (recommended)
- **1.0** = Maximum noise reduction (may affect audio quality)

### Step 3: Analyze

Click the **"Analyze"** button to:
- Detect noise characteristics in your audio
- Analyze video scenes (if video file is selected)
- Generate audio enhancement suggestions
- Display detected scenes and confidence levels

**What happens during analysis:**
- Audio analysis takes 1-2 seconds per 10 seconds of audio
- Video analysis takes 2-3 seconds per 10 seconds of video
- A progress bar shows the analysis status
- Status updates appear at the bottom

### Step 4: Review Results

After analysis completes, you'll see:
- **Detected Scenes** - What the video analysis found (e.g., "outdoor", "storm")
- **Confidence Level** - How confident the detection is (0-100%)
- **Suggestions** - Recommended audio enhancements

### Step 5: Process or Export

Choose one of two actions:

#### Option A: Process Audio
Click **"Process Audio"** to:
- Apply noise reduction to your audio file
- Save the processed audio as `processed_[filename].wav`
- Use this for quick noise reduction without REAPER

#### Option B: Export to REAPER
Click **"Export to REAPER"** to:
- Generate processing instructions in JSON format
- Create separate audio and video tracks
- Include enhancement tracks with ambient sounds
- Export file saved to `~/.reaper_audio_enhancement/exports/`
- Import the export file into REAPER for final mixing

---

## Understanding the Results

### Scene Detection

The tool detects 6 scene types:

| Scene Type | Indicators | Suggested Audio |
|-----------|-----------|-----------------|
| **Storm** | Dark sky, high contrast, blue tones | Thunder, rain, wind |
| **Car Ride** | Interior view, motion blur, gray tones | Car engine, wind, road noise |
| **Outdoor** | Bright, natural lighting, blue sky | Wind, birds, nature ambience |
| **Indoor** | Enclosed space, artificial lighting | Room tone, subtle ambience |
| **Traffic** | Urban environment, vehicles, motion | Traffic noise, car horns |
| **Quiet** | Calm, minimal activity, low contrast | Silence, subtle ambience |

### Confidence Scores

- **80-100%** - High confidence, strong suggestion
- **60-80%** - Moderate confidence, consider the suggestion
- **40-60%** - Low confidence, use with caution
- **Below 40%** - Very low confidence, may not be accurate

---

## Workflow Examples

### Example 1: Interview with Wind Noise

**Scenario**: You recorded an outdoor interview but there's unwanted wind noise.

**Steps**:
1. Load audio file: `interview.wav`
2. Load video file: `interview.mp4`
3. Set noise reduction to 0.5
4. Click "Analyze"
5. Tool detects: "outdoor" scene with wind noise
6. Suggestions: Add wind ambience to mask original wind
7. Click "Export to REAPER"
8. Import into REAPER and adjust volumes

**Result**: Professional-sounding interview with natural wind ambience

### Example 2: Podcast with Background Hum

**Scenario**: Your podcast has a constant 60Hz hum from electrical equipment.

**Steps**:
1. Load audio file: `podcast.wav`
2. Skip video file (not needed)
3. Set noise reduction to 0.7
4. Click "Analyze"
5. Tool detects: Constant low-frequency noise
6. Click "Process Audio"
7. Use processed file in your podcast

**Result**: Clean podcast audio without hum

### Example 3: Video with Missing Ambience

**Scenario**: You have a video of a storm but the audio doesn't capture the wind.

**Steps**:
1. Load audio file: `storm_audio.wav`
2. Load video file: `storm_video.mp4`
3. Set noise reduction to 0.3 (light reduction)
4. Click "Analyze"
5. Tool detects: "storm" scene
6. Suggestions: Add wind and rain sounds
7. Click "Export to REAPER"
8. Create separate tracks for original audio and wind/rain
9. Mix to taste in REAPER

**Result**: Video with enhanced audio that matches the visual content

---

## Tips for Best Results

### Audio Selection
- Use high-quality source audio (WAV preferred)
- Ensure audio is properly normalized
- Avoid heavily compressed audio

### Video Selection
- Use clear, well-lit video for better scene detection
- Ensure video matches the audio content
- Longer videos (10+ seconds) provide better analysis

### Noise Reduction Settings
- Start with 0.5 (moderate) and adjust as needed
- Higher values may introduce artifacts
- Always preview before finalizing

### REAPER Integration
- Import the generated export file into REAPER
- Adjust track volumes to taste
- Use REAPER's mixing tools for final polish
- Save your REAPER project for future reference

---

## Troubleshooting

### Issue: "No file selected" error
**Solution**: Make sure you've selected an audio file before clicking Analyze

### Issue: Analysis is slow
**Solution**: 
- Use shorter video files (under 1 minute)
- Close other applications to free up CPU
- Reduce video resolution if possible

### Issue: Noise reduction sounds unnatural
**Solution**:
- Reduce the noise reduction strength slider
- Try values between 0.3-0.5 instead of maximum
- Use "Export to REAPER" for more control

### Issue: Scene detection is wrong
**Solution**:
- Ensure video clearly shows the scene
- Try with better-lit video
- Scene detection uses basic heuristics (not AI)

### Issue: Can't import export file to REAPER
**Solution**:
- Check that REAPER is running
- Verify OSC is enabled in REAPER preferences
- Try manual import using File > Open

---

## Audio Library

The tool includes pre-recorded ambient sounds:

- **wind.wav** - Wind ambience (useful for outdoor/storm scenes)
- **rain.wav** - Rain sound (useful for storm scenes)
- **thunder.wav** - Thunder sound (useful for storm scenes)
- **car_engine.wav** - Car engine noise (useful for car ride scenes)
- **ambient_nature.wav** - Nature ambience (useful for outdoor scenes)

These sounds are automatically suggested based on detected scenes.

---

## Settings & Configuration

### Configuration File
Settings are stored in: `~/.reaper_audio_enhancement/settings.json`

### Adjustable Settings
- `noise_reduction_strength` - Default noise reduction (0.0-1.0)
- `fade_duration` - Fade in/out duration in seconds
- `osc_host` - REAPER OSC host address
- `osc_port` - REAPER OSC port number

### Changing Settings
Edit the JSON file directly or the settings will be updated when you adjust the slider in the GUI.

---

## Advanced Features

### Separate Tracks in REAPER

When you export to REAPER, you get:

1. **Original Audio Track**
   - Your original audio with noise reduction applied
   - Volume can be reduced to blend with enhancements

2. **Video Track**
   - Your video file for reference
   - Used for scene detection

3. **Enhancement Tracks**
   - Contextual ambient sounds
   - Independent fade and volume control
   - Can be muted or adjusted individually

### Fade Control

Each enhancement track has:
- **Fade In** - Smooth transition at the start (default: 0.5s)
- **Fade Out** - Smooth transition at the end (default: 0.5s)
- Prevents abrupt audio changes

### Volume Control

- **Original Audio** - Reduced by 30% to make room for enhancements
- **Enhancement Tracks** - Set to 70% volume for natural blending
- Fully adjustable in REAPER after import

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+O` | Open audio file |
| `Cmd+V` | Open video file |
| `Cmd+A` | Start analysis |
| `Cmd+P` | Process audio |
| `Cmd+E` | Export to REAPER |

---

## Getting Help

### Documentation
- See `README.md` for project overview
- See `QUICKSTART.md` for quick start
- See `TRACK_ARCHITECTURE.md` for track details

### Common Questions

**Q: Do I need a video file?**
A: No, video is optional. The tool works with audio alone.

**Q: Can I use MP3 files?**
A: Yes, MP3, WAV, and FLAC formats are supported.

**Q: How long does analysis take?**
A: Typically 3-5 seconds for a 10-second file.

**Q: Can I undo changes?**
A: Original files are never modified. Processed files are saved separately.

**Q: Is there a limit to file length?**
A: No hard limit, but very long files may take longer to analyze.

---

## Next Steps

1. **Try the Sample Files**
   - Use `assets/sample_files/sample_audio.wav`
   - Use `assets/sample_files/sample_video.mp4`
   - See how the tool works with provided examples

2. **Experiment with Settings**
   - Try different noise reduction strengths
   - See how video affects suggestions
   - Find the best settings for your use case

3. **Integrate with REAPER**
   - Export your first project
   - Import into REAPER
   - Adjust and finalize in REAPER

4. **Provide Feedback**
   - Let us know what works well
   - Suggest improvements
   - Help shape future versions

---

## Support

For issues or questions:
1. Check this user guide
2. Review the documentation files
3. Check the status messages in the application
4. Review error messages for clues

---

**Happy audio enhancing!**
