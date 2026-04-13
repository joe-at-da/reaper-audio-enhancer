# REAPER Integration Guide

## Overview

The REAPER Audio Enhancement Tool exports audio processing instructions as JSON files that can be imported into REAPER to create organized tracks with noise reduction and audio suggestions.

---

## What is the Export File?

When you click **"Export to REAPER"**, the tool creates a JSON file containing:

1. **Original Audio Track**
   - Your audio file with noise reduction applied
   - Volume reduced to make room for enhancements

2. **Video Track**
   - Your video file (for reference and synchronization)
   - No processing applied

3. **Enhancement Tracks**
   - Suggested ambient sounds based on detected scenes
   - Each with fade in/out and volume settings
   - Examples: wind, rain, thunder, car engine, nature ambience

---

## File Location

Export files are saved to:
```
~/.reaper_audio_enhancement/exports/export_YYYYMMDD_HHMMSS.json
```

**Example**:
```
~/.reaper_audio_enhancement/exports/export_20260413_210143.json
```

---

## What's Inside the Export File?

### File Structure

```json
{
  "timestamp": "2026-04-13T21:01:43.478000",
  "version": "0.1.0",
  "audio_track": {
    "name": "Original Audio",
    "type": "audio",
    "file": "/path/to/processed_audio.wav",
    "processing": {
      "noise_reduction": {
        "enabled": true,
        "strength": 0.5
      }
    }
  },
  "video_track": {
    "name": "Video",
    "type": "video",
    "file": "/path/to/video.mp4"
  },
  "enhancement_tracks": [
    {
      "name": "Enhancement - wind",
      "type": "audio",
      "file": "/path/to/wind.wav",
      "start_time": 0.0,
      "duration": 10.0,
      "volume": 0.7,
      "fade_in": 0.5,
      "fade_out": 0.5
    }
  ]
}
```

---

## How to Import into REAPER

### Method 1: Manual Import (Recommended for Now)

Since REAPER integration is still being developed, you can manually import the files:

#### Step 1: Create Tracks in REAPER

1. Open REAPER
2. Create a new project
3. Create three tracks:
   - **Track 1**: Audio (for processed audio)
   - **Track 2**: Video (for video reference)
   - **Track 3+**: Audio (for enhancement tracks)

#### Step 2: Add Files to Tracks

1. **Original Audio Track**
   - Right-click track → Insert media file
   - Select `processed_[filename].wav` from the export
   - This is your noise-reduced audio

2. **Video Track**
   - Right-click track → Insert media file
   - Select your video file
   - This provides visual reference

3. **Enhancement Tracks**
   - For each suggested audio:
     - Create a new audio track
     - Insert the audio file (e.g., wind.wav, rain.wav)
     - Set fade in/out as suggested in the export file
     - Adjust volume to blend with original

#### Step 3: Adjust Volumes

Based on the export file:
- **Original Audio**: Reduce volume by ~3dB to make room for enhancements
- **Enhancement Tracks**: Set to ~70% volume for natural blending
- Adjust as needed for your mix

#### Step 4: Set Fade Points

For each enhancement track:
- **Fade In**: 0.5 seconds at the start
- **Fade Out**: 0.5 seconds at the end
- This prevents abrupt audio changes

---

## Understanding the Track Structure

### Original Audio Track

**Purpose**: Your audio with noise reduction applied

**What it contains**:
- Your original audio file
- Noise reduction applied (50% strength by default)
- Wind noise and electrical hum reduced
- Speech clarity improved

**How to use**:
- Reduce volume to -3dB to -6dB
- This makes room for enhancement tracks
- Can be muted for audio-only enhancement mode

### Video Track

**Purpose**: Visual reference for synchronization

**What it contains**:
- Your video file
- No audio processing
- Scene information (outdoor, storm, etc.)

**How to use**:
- Keep at 0dB volume (no audio output needed)
- Use for visual reference while editing
- Helps ensure audio matches video content

### Enhancement Tracks

**Purpose**: Contextual ambient sounds to improve audio

**What they contain**:
- Suggested ambient sounds (wind, rain, thunder, etc.)
- Based on detected video scenes
- Pre-configured fade and volume settings

**How to use**:
- Each track is independent
- Adjust volume to taste
- Modify fade points as needed
- Can be muted to compare with/without

---

## Example: Interview with Wind Noise

### Scenario
You recorded an outdoor interview but there's unwanted wind noise.

### What the Tool Does
1. **Analyzes audio** → Detects wind noise
2. **Analyzes video** → Detects outdoor scene
3. **Suggests audio** → Wind ambience to mask original wind
4. **Exports** → JSON with three tracks

### REAPER Tracks Created

| Track | Content | Volume | Fade |
|-------|---------|--------|------|
| 1 | Processed interview (wind reduced) | -3dB | None |
| 2 | Video (reference) | 0dB | None |
| 3 | Wind ambience | -6dB | 0.5s in/out |

### Result
- Original wind noise reduced by 50%
- Natural wind ambience added
- Professional sound design
- Easy to adjust or remove

---

## Troubleshooting

### Issue: Files Not Found

**Problem**: REAPER can't find the audio/video files

**Solution**:
1. Check file paths in the JSON export
2. Ensure files haven't been moved
3. Use absolute paths if relative paths don't work
4. Copy files to a project folder if needed

### Issue: Audio Out of Sync

**Problem**: Enhancement tracks don't align with original audio

**Solution**:
1. Check start times in the JSON export
2. Manually adjust track timing in REAPER
3. Use REAPER's sync tools to align tracks
4. Verify video and audio are synchronized

### Issue: Volume Levels Wrong

**Problem**: Enhancement tracks are too loud or too quiet

**Solution**:
1. Adjust track volume in REAPER
2. Use REAPER's mixer for precise control
3. Reference the suggested volumes in the export file
4. Use A/B comparison to find the right balance

### Issue: Fade Points Not Working

**Problem**: Fade in/out not applied correctly

**Solution**:
1. Manually create fade points in REAPER
2. Use REAPER's envelope tool
3. Set fade duration as specified in export file
4. Test with playback to verify

---

## Advanced Features

### A/B Comparison

To compare with and without enhancements:
1. Mute enhancement tracks
2. Listen to original audio only
3. Unmute enhancement tracks
4. Compare the difference

### Custom Adjustments

You can modify:
- Track volumes
- Fade points
- Track order
- Enhancement selection
- Timing and synchronization

### Exporting Final Mix

Once you're happy with the mix:
1. Select all tracks
2. File → Render → Render to file
3. Choose format (WAV, MP3, etc.)
4. Export your final audio

---

## Future Improvements

### Planned Features
- Direct REAPER plugin integration
- One-click track creation
- Automatic volume balancing
- Real-time preview
- Custom audio library support

### Current Limitations
- Manual track creation required
- JSON format only (no direct import)
- No real-time preview in REAPER
- Limited to pre-recorded audio library

---

## Tips for Best Results

1. **Use High-Quality Audio**
   - Start with good source material
   - Noise reduction works better with clear audio

2. **Adjust Noise Reduction Strength**
   - 0.3-0.5: Light reduction (recommended)
   - 0.5-0.7: Moderate reduction
   - 0.7-1.0: Aggressive reduction (may affect quality)

3. **Balance Volumes Carefully**
   - Original audio: -3dB to -6dB
   - Enhancement tracks: -6dB to -12dB
   - Adjust to taste

4. **Use Fade Points**
   - Prevents abrupt audio changes
   - Creates smooth transitions
   - Typical: 0.5 seconds

5. **Test Before Finalizing**
   - Listen to the full mix
   - Compare with original
   - Make adjustments as needed

---

## Getting Help

### Documentation
- See `USER_GUIDE.md` for application usage
- See `QUICKSTART.md` for quick start
- See `DEMO_MODE.md` for demo mode

### Troubleshooting
- Check log files for errors
- Verify file paths and formats
- Test with sample files first

---

## Summary

The export file provides all the information needed to create professional audio tracks in REAPER:
- ✓ Processed audio with noise reduction
- ✓ Video reference for synchronization
- ✓ Enhancement tracks with suggestions
- ✓ Fade and volume settings
- ✓ Ready for manual import and adjustment

**Next Steps**:
1. Export from the tool
2. Create tracks in REAPER
3. Import audio/video files
4. Adjust volumes and fades
5. Export final mix

---

**For questions or issues, refer to the comprehensive documentation provided with the application.**
