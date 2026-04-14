# Audio Library Setup Guide

**Status**: Audio Library Manager implemented, ready for expansion

---

## Overview

The application now includes an Audio Library Manager system for managing audio suggestions. The current library contains 5 basic sounds, and can be expanded with custom audio files.

---

## Current Audio Library

Location: `assets/audio_library/`

**Available Sounds**:
- ambient_nature.wav
- car_engine.wav
- rain.wav
- thunder.wav
- wind.wav

---

## Audio Library Manager

**File**: `src/utils/audio_library_manager.py`

**Features**:
- Check if library is installed
- List available sounds
- Get specific sound file
- Validate library integrity
- Provide installation instructions
- Get library status

**Usage**:
```python
from src.utils.audio_library_manager import get_audio_library_manager

manager = get_audio_library_manager()

# Check if installed
if manager.is_installed():
    print("Audio library is installed")

# Get available sounds
sounds = manager.get_available_sounds()
print(sounds)  # {'wind': '/path/to/wind.wav', ...}

# Get specific sound
wind_file = manager.get_sound('wind')

# Get status
status = manager.get_status()
print(status)
```

---

## Installation Process

### Current: Manual Setup

1. Download audio files from recommended sources
2. Place files in: `assets/audio_library/`
3. Restart application
4. Library is automatically detected

### Recommended Sources with Direct Download Links

**Mixkit.co** (Recommended - No registration required)
- URL: https://mixkit.co/free-sound-effects/
- License: Free to use
- Rain sounds: https://mixkit.co/free-sound-effects/rain/
- Thunder sounds: https://mixkit.co/free-sound-effects/thunder/
- Wind sounds: https://mixkit.co/free-sound-effects/wind/
- Ambient sounds: https://mixkit.co/free-sound-effects/ambient/
- Car sounds: https://mixkit.co/free-sound-effects/car/

**Freesound.org**
- URL: https://freesound.org
- License: Creative Commons (check individual licenses)
- Search: "wind", "rain", "thunder", "snow", "ambient"
- Note: Requires free account to download

**Pixabay.com**
- URL: https://pixabay.com/sound-effects
- License: Free to use
- Search: "wind", "rain", "thunder", "snow", "ambient"

**Zapsplat.com**
- URL: https://www.zapsplat.com
- License: Free to use
- Search: "wind", "rain", "thunder", "snow", "ambient"

---

## Adding Custom Sounds

### Step 1: Download Audio Files

**Quick Start (Mixkit - Easiest)**:
1. Go to: https://mixkit.co/free-sound-effects/rain/
2. Click on a rain sound you like
3. Click "Download" button (no registration needed)
4. Repeat for: thunder, wind, car engine, ambient sounds
5. Files will be downloaded as `.wav` files

**Alternative (Freesound)**:
1. Create free account at https://freesound.org
2. Search for: "wind", "rain", "thunder", "car engine", "ambient"
3. Download sounds in WAV format
4. Check license is Creative Commons (free to use)

**Recommended Sounds to Download**:
- **Rain**: Heavy rain, light rain, rain on window
- **Thunder**: Thunder rumble, thunder strike, thunderstorm
- **Wind**: Wind howling, strong wind, gentle breeze
- **Car Engine**: Car driving, car engine, traffic
- **Ambient**: Forest ambience, nature sounds, urban ambience

### Step 2: Place Files
1. Copy audio files to: `assets/audio_library/`
2. Name files descriptively (e.g., `wind_howling.wav`, `rain_heavy.wav`)

### Step 3: Restart Application
1. Close the application
2. Restart the application
3. New sounds will be automatically detected

### Step 4: Use in Suggestions
The tool will now suggest these sounds when analyzing audio/video.

---

## File Format Requirements

**Recommended**:
- Format: WAV (uncompressed)
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit
- Duration: 5-30 seconds
- Channels: Mono or Stereo

**Also Supported**:
- MP3 (compressed)
- FLAC (lossless)
- OGG (compressed)

---

## Future Enhancements

### Phase 1: Automatic Download (Tomorrow)
- Add button in Settings: "Install Audio Library"
- Download sounds from Freesound API
- Requires: Freesound API key
- Automatic setup

### Phase 2: AI Audio Generation (Tomorrow)
- Generate custom sounds using Stable Audio
- Example: "snowstorm wind sounds, heavy snow falling"
- Requires: Stable Audio API key
- On-demand generation

### Phase 3: API Audio Search (Future)
- Search and download from Freesound API
- Search and download from Epidemic Sound API
- Requires: API keys
- Dynamic library expansion

---

## Settings Integration

**Current**: Library status shown in Settings dialog
- Display: "Audio Library Status"
- Show: "Installed" or "Not Installed"
- Show: Number of available sounds
- Show: List of available sounds

**Future**: Add buttons for:
- "Install Audio Library" - Automatic download
- "Browse Library" - View/manage sounds
- "Add Custom Sounds" - Manual upload

---

## Troubleshooting

### Library Not Detected
- Check files are in: `assets/audio_library/`
- Check files are in WAV format
- Restart application

### Sounds Not Appearing in Suggestions
- Verify library is installed
- Check audio files are valid
- Check file names are descriptive

### Audio Quality Issues
- Use 44100 Hz sample rate
- Use 16-bit depth
- Use WAV format (uncompressed)

---

## API Integration (Future)

### Freesound API
```python
# Example (future implementation)
from freesound_client import FreesoundClient

client = FreesoundClient()
client.set_token("YOUR_API_KEY")

sounds = client.text_search(query="wind", page_size=5)
for sound in sounds:
    # Download and add to library
    pass
```

### Stable Audio API
```python
# Example (future implementation)
from stable_audio_tools import StableAudioClient

client = StableAudioClient(api_key="YOUR_API_KEY")

audio = client.generate(
    prompt="snowstorm wind sounds, heavy snow falling",
    duration=10
)
# Save to library
```

---

## Summary

✓ Audio Library Manager created  
✓ Current library: 5 basic sounds  
✓ Manual installation supported  
✓ Localization added (English + Ukrainian)  
✓ Foundation for automatic download  
✓ Foundation for AI generation  
✓ Foundation for API search  

**Next Steps**:
1. Add more sounds to library manually
2. Implement automatic download (tomorrow)
3. Implement AI audio generation (tomorrow)
4. Implement API audio search (future)

The audio library system is ready for expansion!
