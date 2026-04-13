# Sample Files Information

## Overview

The application includes realistic sample audio and video files designed for testing and onboarding. These files have been carefully created to demonstrate the full capabilities of the noise reduction and audio suggestion features.

---

## Sample Audio File

**File**: `assets/sample_files/sample_audio.wav`

### Content
- **Duration**: 10 seconds
- **Sample Rate**: 22,050 Hz
- **Format**: WAV (uncompressed)

### Audio Components
1. **Simulated Speech** (Primary Content)
   - Multiple frequency components (200 Hz, 400 Hz, 800 Hz, 1600 Hz)
   - Amplitude modulation to simulate natural speech patterns
   - Realistic speech envelope

2. **Wind Noise** (Problem to Solve)
   - Low-frequency noise (80 Hz, 120 Hz)
   - Random noise component
   - Simulates outdoor wind interference

3. **Electrical Hum** (Secondary Noise)
   - 60 Hz sine wave
   - Simulates common electrical interference
   - Easy to detect and remove

### Why This Works
- **Realistic**: Contains actual speech-like content, not just tones
- **Noisy**: Has multiple noise sources to demonstrate noise reduction
- **Detectable**: Noise characteristics are clear and analyzable
- **Testable**: Good for verifying noise reduction effectiveness

---

## Sample Video File

**File**: `assets/sample_files/sample_video.mp4`

### Content
- **Duration**: 10 seconds
- **Resolution**: 640 × 480 pixels
- **Frame Rate**: 30 FPS
- **Format**: MP4 (H.264 codec)

### Scene Progression

**0-3 seconds: Outdoor - Clear**
- Blue sky background
- Green trees (landscape elements)
- Scene type: "outdoor"
- Confidence: High

**3-6 seconds: Storm Approaching**
- Gray sky background
- Transition from clear to stormy
- Scene type: "storm"
- Confidence: Medium

**6-10 seconds: Heavy Storm**
- Dark sky background
- Rain effect (diagonal lines)
- Scene type: "storm"
- Confidence: High

### Visual Elements
- Color gradients for scene transitions
- Text labels showing scene type and time
- Visual effects (trees, rain) for realism
- Timestamp display for reference

### Why This Works
- **Clear Transitions**: Scene changes are obvious and detectable
- **Realistic**: Simulates actual outdoor to storm progression
- **Synchronized**: Matches the audio content (outdoor → storm)
- **Testable**: Good for verifying scene detection

---

## Audio-Video Synchronization

### Matching Content
The sample audio and video are designed to work together:

| Time | Audio | Video | Suggestion |
|------|-------|-------|-----------|
| 0-3s | Speech + wind | Outdoor scene | Wind ambience |
| 3-6s | Speech + wind + hum | Storm approaching | Wind + rain |
| 6-10s | Speech + wind + hum | Heavy storm | Wind + rain + thunder |

### How They Work Together
1. **Audio Analysis** detects wind noise and electrical hum
2. **Video Analysis** detects outdoor → storm transition
3. **Combination** suggests adding wind/rain sounds
4. **Result** creates a cohesive audio-visual experience

---

## Ambient Sound Library

The application includes 5 pre-recorded ambient sounds for suggestions:

### 1. Wind Sound
**File**: `assets/audio_library/wind.wav`
- **Duration**: 5 seconds
- **Frequency**: Low (60-100 Hz)
- **Use**: Outdoor, storm, car ride scenes
- **Characteristics**: Low-frequency noise with sine wave components

### 2. Rain Sound
**File**: `assets/audio_library/rain.wav`
- **Duration**: 5 seconds
- **Frequency**: Mid-range (150-300 Hz)
- **Use**: Storm scenes
- **Characteristics**: White noise with structured components

### 3. Thunder Sound
**File**: `assets/audio_library/thunder.wav`
- **Duration**: 5 seconds
- **Frequency**: Very low (50-100 Hz)
- **Use**: Storm scenes
- **Characteristics**: Deep bass burst with noise

### 4. Car Engine Sound
**File**: `assets/audio_library/car_engine.wav`
- **Duration**: 5 seconds
- **Frequency**: Mid (120-360 Hz)
- **Use**: Car ride, traffic scenes
- **Characteristics**: Harmonic series with noise

### 5. Nature Ambience
**File**: `assets/audio_library/ambient_nature.wav`
- **Duration**: 5 seconds
- **Frequency**: Mid-range (100-400 Hz)
- **Use**: Outdoor, quiet scenes
- **Characteristics**: Multiple frequency components

---

## How to Use Sample Files

### In Demo Mode
```bash
bash launch.sh demo
```
- Audio and video automatically pre-loaded
- Click "Analyze" to see detection results
- Click "Process Audio" to reduce noise
- Click "Export to REAPER" to create tracks

### Manual Testing
```bash
bash launch.sh
```
- Click "Browse Audio" → Select `sample_audio.wav`
- Click "Browse Video" → Select `sample_video.mp4`
- Adjust noise reduction strength
- Click "Analyze"

### Expected Results

**After Analysis**:
- Noise profile detected (wind + hum)
- Scenes detected (outdoor → storm)
- Suggestions generated (wind, rain, thunder)
- Confidence scores shown

**After Processing**:
- Wind noise reduced by 50% (default)
- Speech clarity improved
- Electrical hum reduced
- File saved as `processed_sample_audio.wav`

**After Export**:
- JSON export file created
- Three tracks generated:
  - Original audio (processed)
  - Video (reference)
  - Enhancement tracks (wind, rain, etc.)

---

## Regenerating Sample Files

If you want to recreate the sample files:

```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
source venv/bin/activate
python create_samples.py
```

This will:
1. Create new `sample_audio.wav` with speech + wind + hum
2. Create new `sample_video.mp4` with outdoor → storm transition
3. Create 5 ambient sounds in audio library

---

## Technical Details

### Audio Generation
- **Sample Rate**: 22,050 Hz (CD quality)
- **Bit Depth**: 16-bit (standard WAV)
- **Channels**: Mono
- **Amplitude**: Normalized to prevent clipping

### Video Generation
- **Codec**: H.264 (MP4)
- **Color Space**: BGR (OpenCV format)
- **Frame Size**: 640 × 480 (VGA)
- **Frame Rate**: 30 FPS

### Noise Characteristics
- **Wind Noise**: 80-120 Hz (low frequency)
- **Electrical Hum**: 60 Hz (power line frequency)
- **Speech**: 200-1600 Hz (typical range)

---

## Limitations

### Current Sample Files
- **Synthetic**: Generated, not recorded
- **Simple**: Limited complexity compared to real recordings
- **Mono**: Single channel (not stereo)
- **Short**: Only 10 seconds (for quick testing)

### What They Don't Include
- Real speech (only simulated)
- Real environmental sounds
- Stereo or surround sound
- Long-duration content
- Multiple speakers

### For Production Use
For real-world testing, consider:
- Recording actual audio/video
- Using royalty-free samples from Pixabay, Freesound, etc.
- Including various noise types
- Testing with longer files
- Using stereo/surround content

---

## Improving Sample Files

### Option 1: Use Real Recordings
Download from:
- **Pixabay**: https://pixabay.com/sound-effects/
- **Freesound**: https://freesound.org/
- **Mixkit**: https://mixkit.co/free-sound-effects/
- **Zapsplat**: https://www.zapsplat.com/

### Option 2: Record Your Own
- Record outdoor audio with wind noise
- Record video of outdoor/storm scenes
- Ensure audio and video are synchronized
- Export as WAV (audio) and MP4 (video)

### Option 3: Modify create_samples.py
Edit the script to:
- Add more frequency components
- Increase noise levels
- Change scene transitions
- Add more visual elements

---

## Troubleshooting

### Issue: "No audio suggestions generated"
**Cause**: Sample audio might be too simple or noise not detected
**Solution**: 
- Check audio content with `python create_samples.py`
- Verify noise levels are sufficient
- Try with real audio files

### Issue: "Scene detection failed"
**Cause**: Video might not have clear color differences
**Solution**:
- Check video with video player
- Verify color transitions are visible
- Try with real video files

### Issue: "Processed audio sounds wrong"
**Cause**: Noise reduction strength might be too high
**Solution**:
- Reduce noise reduction strength (try 0.3-0.5)
- Check original audio quality
- Use real audio files for better results

---

## Next Steps

1. **Test with Sample Files**
   ```bash
   bash launch.sh demo
   ```

2. **Try Different Settings**
   - Adjust noise reduction slider
   - See how it affects output

3. **Export to REAPER**
   - Click "Export to REAPER"
   - Import into REAPER
   - Adjust and mix

4. **Use Real Files**
   - Record your own audio/video
   - Or download from royalty-free sources
   - Test with actual content

---

## Summary

The sample files are designed to:
- ✓ Demonstrate all features
- ✓ Provide realistic test content
- ✓ Show noise reduction in action
- ✓ Demonstrate scene detection
- ✓ Enable quick onboarding

**Perfect for**: Testing, demos, onboarding, and feature verification.

---

**For questions or improvements, refer to the main documentation files.**
