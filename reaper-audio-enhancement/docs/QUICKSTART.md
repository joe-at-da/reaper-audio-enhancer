# Quick Start Guide

## Installation

### macOS
```bash
cd reaper-audio-enhancement
bash installer/install_macos.sh
```

### Windows
```cmd
cd reaper-audio-enhancement
installer\install_windows.bat
```

## Running the Application

### Method 1: Simple Launcher (Recommended)
```bash
cd reaper-audio-enhancement
bash launch.sh
```

### Method 2: Manual Launch
```bash
cd reaper-audio-enhancement
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

python run.py
```

### Method 3: Setup Wizard
```bash
source venv/bin/activate
python installer/setup_wizard.py
```

## Features

### 1. Audio Analysis
- Load audio files (WAV, MP3, FLAC)
- Detect noise characteristics
- Identify problematic audio regions
- View spectral analysis

### 2. Video Integration (Optional)
- Load video files (MP4, MOV, AVI)
- Detect scenes (storm, car ride, outdoor, indoor, traffic, quiet)
- Get scene-based audio suggestions

### 3. Noise Reduction
- Spectral subtraction algorithm
- Adjustable noise reduction strength (0.0 - 1.0)
- Fade in/out to prevent artifacts
- Preview before processing

### 4. Audio Suggestions
- Scene-aware ambient sound suggestions
- Pre-loaded audio library (wind, rain, thunder, car engine, nature sounds)
- Volume and fade control
- Accept/reject workflow

### 5. REAPER Export
- Export processing instructions as JSON
- Separate audio and video tracks
- Ready for REAPER import

## Sample Files

Sample audio and video files are included in `assets/sample_files/`:
- `sample_audio.wav` - Audio with background noise
- `sample_video.mp4` - Video with scene transitions (clear sky → storm)

Ambient sounds are in `assets/audio_library/`:
- `wind.wav`
- `rain.wav`
- `thunder.wav`
- `car_engine.wav`
- `ambient_nature.wav`

## Workflow Example

1. **Launch Application**
   ```bash
   python src/main.py
   ```

2. **Load Files**
   - Click "Browse Audio" → select `assets/sample_files/sample_audio.wav`
   - Click "Browse Video" → select `assets/sample_files/sample_video.mp4`

3. **Analyze**
   - Click "Analyze"
   - Wait for analysis to complete
   - View detected scenes and suggestions

4. **Process Audio**
   - Adjust "Noise Reduction Strength" slider if needed
   - Click "Process Audio"
   - Processed file saved as `processed_sample_audio.wav`

5. **Export to REAPER**
   - Click "Export to REAPER"
   - Export saved to `~/.reaper_audio_enhancement/exports/`
   - Import into REAPER project

## Configuration

Settings are stored in `.config/settings.json`:
- `reaper_path` - Path to REAPER installation
- `osc_host` - OSC server host (default: 127.0.0.1)
- `osc_port` - OSC server port (default: 9000)
- `noise_reduction_strength` - Default reduction strength (0.0-1.0)
- `fade_duration` - Fade in/out duration in seconds
- `audio_library_path` - Path to ambient sounds
- `sample_files_path` - Path to sample files

## Testing

Run unit tests:
```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## Troubleshooting

### PyQt5 Display Issues (macOS)
If you see Qt platform plugin errors, ensure you're using the system Python or have proper display settings.

### Audio File Not Loading
- Ensure file format is supported (WAV, MP3, FLAC)
- Check file permissions
- Verify file is not corrupted

### Video Processing Slow
- Video analysis is CPU-intensive
- Reduce video resolution or duration for faster processing
- Use shorter keyframe intervals

## Next Steps

- Integrate with REAPER via ReaScript
- Add ML-based noise reduction (Silero, Demucs)
- Implement real-time processing
- Add batch processing for multiple files
- Create installers for distribution

## Support

For issues or questions, check the main README.md or review the code documentation.
