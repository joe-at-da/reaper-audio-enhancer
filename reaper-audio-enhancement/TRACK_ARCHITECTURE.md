# Track Architecture - Audio & Video Separation

## Overview

The REAPER Audio Enhancement Plugin is designed with separate audio and video track management to provide maximum flexibility and control over the audio/video workflow.

---

## Track Organization

### Track Structure

The plugin creates and manages three types of tracks in REAPER:

```
Track 1: Original Audio
├── Type: Audio
├── Purpose: Original noisy audio
├── Processing: Optional noise reduction
└── Output: Can be muted or reduced in volume

Track 2: Video
├── Type: Video
├── Purpose: Video reference
├── Processing: None
└── Output: Visual reference for editing

Track 3+: Enhancement Tracks (Multiple)
├── Type: Audio
├── Purpose: Contextual ambient sounds
├── Processing: Fade in/out, volume control
└── Output: Blended with original or replacement
```

---

## Data Structure

### Export Format (JSON)

The plugin exports track information in JSON format for REAPER import:

```json
{
  "timestamp": "2026-04-13T19:57:34.123456",
  "version": "0.1.0",
  "audio_track": {
    "name": "Original Audio",
    "type": "audio",
    "file": "/path/to/original_audio.wav",
    "processing": {
      "noise_reduction": {
        "enabled": true,
        "strength": 0.5,
        "output_file": "/path/to/processed_audio.wav"
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
      "name": "Enhancement - storm",
      "type": "audio",
      "file": "/path/to/wind.wav",
      "start_time": 0.0,
      "duration": 10.0,
      "volume": 0.7,
      "fade_in": 0.5,
      "fade_out": 0.5
    },
    {
      "name": "Enhancement - ambient",
      "type": "audio",
      "file": "/path/to/ambient_nature.wav",
      "start_time": 5.0,
      "duration": 5.0,
      "volume": 0.5,
      "fade_in": 0.3,
      "fade_out": 0.3
    }
  ],
  "suggestions": [
    {
      "scene": "storm",
      "confidence": 0.8,
      "audio_file": "wind.wav",
      "audio_path": "/path/to/wind.wav",
      "fade_in": 0.5,
      "fade_out": 0.5,
      "volume_reduction": 0.3,
      "priority": 0.8,
      "accepted": true
    }
  ]
}
```

---

## Workflow: Separate Tracks

### Step 1: Load Files
```
User selects:
├── Audio File (e.g., interview_with_wind.wav)
└── Video File (e.g., outdoor_interview.mp4)
```

### Step 2: Analysis
```
Plugin analyzes:
├── Audio: Detects wind noise, background hum
├── Video: Detects outdoor scene, wind indicators
└── Suggestions: Recommends wind sound replacement
```

### Step 3: Processing
```
Plugin creates:
├── Track 1 (Original Audio)
│   └── Original audio with noise reduction applied
├── Track 2 (Video)
│   └── Video file for reference
└── Track 3 (Enhancement)
    └── Wind sound with fade and volume control
```

### Step 4: REAPER Import
```
REAPER project structure:
├── Track 1: Original Audio
│   ├── Item: processed_interview.wav (0:00 - 10:00)
│   └── Volume: -3dB (reduced to make room for enhancement)
├── Track 2: Video
│   ├── Item: outdoor_interview.mp4 (0:00 - 10:00)
│   └── Volume: 0dB (reference only)
└── Track 3: Enhancement - Wind
    ├── Item: wind.wav (0:00 - 10:00)
    ├── Volume: -6dB (blended with original)
    ├── Fade In: 0.5s
    └── Fade Out: 0.5s
```

---

## Audio Track Management

### Original Audio Track

**Purpose**: Preserve original audio with optional processing

**Features**:
- Noise reduction applied (configurable strength)
- Volume can be reduced to blend with enhancements
- Can be muted for audio-only enhancement mode
- Maintains original timing and synchronization

**Processing Options**:
```python
# From noise_reducer.py
audio_reduced = reducer.apply_noise_reduction(
    audio_path="interview.wav",
    output_path="interview_processed.wav",
    strength=0.5,  # 50% noise reduction
    noise_duration=1.0  # Use first 1 second as noise profile
)
```

**Volume Control**:
```
Original Volume: 0dB
After Enhancement: -3dB to -6dB (to blend with new audio)
Muted: -∞dB (for audio-only replacement)
```

---

## Video Track Management

### Video Track

**Purpose**: Visual reference for scene detection and editing

**Features**:
- Separate from audio processing
- Used for scene detection only
- Provides visual context for audio decisions
- Maintains sync with audio tracks

**Processing**:
```python
# From scene_detector.py
scenes = detector.detect_scenes(
    video_path="interview.mp4",
    interval=1.0  # Analyze every 1 second
)
# Returns: [(timestamp, scene_type, confidence), ...]
```

**Scene Types Detected**:
- `storm` - Outdoor weather, wind indicators
- `car_ride` - Vehicle interior, motion
- `outdoor` - Open air, natural lighting
- `indoor` - Enclosed space, artificial lighting
- `traffic` - Urban environment, vehicles
- `quiet` - Calm, minimal activity

---

## Enhancement Tracks

### Audio Suggestion Tracks

**Purpose**: Add contextual ambient sounds based on video content

**Features**:
- Multiple enhancement tracks possible
- Each track has independent fade and volume control
- Confidence-based ranking for suggestions
- Accept/reject workflow before import

**Enhancement Track Structure**:
```python
{
    "name": "Enhancement - storm",
    "type": "audio",
    "file": "/path/to/wind.wav",
    "start_time": 0.0,      # When to start (seconds)
    "duration": 10.0,       # How long to play (seconds)
    "volume": 0.7,          # Volume level (0.0-1.0)
    "fade_in": 0.5,         # Fade in duration (seconds)
    "fade_out": 0.5,        # Fade out duration (seconds)
}
```

**Fade Envelope Example**:
```
Volume
  1.0 |     ___________
      |    /           \
  0.7 |   /             \
      |  /               \
  0.0 |_/                 \_____
      0    0.5s      9.5s  10s
      ^    ^         ^      ^
      |    |         |      |
      Start Fade In  Fade Out End
```

**Volume Blending**:
```
Original Audio:  -3dB
Enhancement:     -6dB
Combined:        Smooth blend without clipping
```

---

## Separate Track Benefits

### For Audio Editing
- ✓ Independent control of original and enhancement audio
- ✓ Easy muting/soloing of individual elements
- ✓ Separate processing chains per track
- ✓ Non-destructive editing (original preserved)

### For Video Editing
- ✓ Visual reference without audio interference
- ✓ Scene detection based on video content
- ✓ Sync point reference
- ✓ Easy video replacement if needed

### For Workflow
- ✓ Accept/reject suggestions before committing
- ✓ Easy A/B comparison (mute enhancement track)
- ✓ Undo capability (separate tracks)
- ✓ Flexible mixing and balancing

### For Collaboration
- ✓ Clear track organization
- ✓ Easy to understand for other editors
- ✓ Standard REAPER workflow
- ✓ Compatible with other plugins

---

## Track Naming Convention

### Standard Names
```
Track 1: "Original Audio"
Track 2: "Video"
Track 3: "Enhancement - [Scene Type]"
Track 4: "Enhancement - [Scene Type]"
...
```

### Example Project
```
Track 1: Original Audio
Track 2: Video
Track 3: Enhancement - storm
Track 4: Enhancement - ambient
Track 5: Enhancement - traffic
```

---

## Audio Library Organization

### Library Structure
```
assets/audio_library/
├── wind.wav              # For storm, outdoor, car_ride scenes
├── rain.wav              # For storm scenes
├── thunder.wav           # For storm scenes
├── car_engine.wav        # For car_ride, traffic scenes
├── ambient_nature.wav    # For outdoor, quiet scenes
└── [future additions]
```

### Scene-to-Audio Mapping
```python
scene_audio_map = {
    "storm": ["thunder.wav", "rain.wav", "wind.wav"],
    "car_ride": ["car_engine.wav", "wind_driving.wav", "road_noise.wav"],
    "outdoor": ["wind.wav", "birds.wav", "ambient_nature.wav"],
    "indoor": ["room_tone.wav", "ambient_indoor.wav"],
    "traffic": ["traffic.wav", "car_horn.wav", "city_ambience.wav"],
    "quiet": ["silence.wav", "subtle_ambience.wav"],
}
```

---

## Configuration for Tracks

### Default Settings
```json
{
    "noise_reduction_strength": 0.5,
    "fade_duration": 0.5,
    "enhancement_volume": 0.7,
    "original_volume_reduction": 0.3,
    "audio_library_path": "assets/audio_library",
    "sample_files_path": "assets/sample_files"
}
```

### Customization
Users can adjust:
- Noise reduction strength (0.0-1.0)
- Fade in/out duration (0.1-5.0 seconds)
- Enhancement track volume (0.0-1.0)
- Original audio volume reduction (0.0-1.0)

---

## Example Workflow: Interview with Wind

### Scenario
Recording an outdoor interview with unwanted wind noise.

### Analysis
```
Video: Outdoor scene detected (confidence: 0.85)
Audio: Wind noise detected in 2-8 kHz range
Suggestion: Add wind sound to mask original wind
```

### Processing
```
Original Audio Track:
├── Input: interview_raw.wav (wind noise present)
├── Processing: Spectral subtraction (strength: 0.5)
└── Output: interview_processed.wav (wind reduced)

Enhancement Track:
├── Source: wind.wav (from library)
├── Duration: Full interview length
├── Volume: -6dB (blended)
├── Fade: 0.5s in/out
└── Purpose: Natural wind ambience
```

### REAPER Project
```
Track 1: Original Audio
├── interview_processed.wav (0:00-5:00)
└── Volume: -3dB

Track 2: Video
├── interview.mp4 (0:00-5:00)
└── Volume: 0dB

Track 3: Enhancement - Wind
├── wind.wav (0:00-5:00)
├── Volume: -6dB
├── Fade In: 0.5s
└── Fade Out: 0.5s
```

### Result
- Original wind noise reduced by 50%
- Natural wind ambience added
- Smooth fade in/out
- Professional sound design
- Easy to adjust or remove

---

## Technical Implementation

### Track Creation in REAPER
```python
# From osc_client.py
osc_client = ReaperOSCClient()
osc_client.connect()

# Create audio track
osc_client.create_track("Original Audio", track_type="audio")
osc_client.set_track_name(0, "Original Audio")

# Create video track
osc_client.create_track("Video", track_type="video")
osc_client.set_track_name(1, "Video")

# Create enhancement track
osc_client.create_track("Enhancement - storm", track_type="audio")
osc_client.set_track_name(2, "Enhancement - storm")
```

### Export Generation
```python
# From export_generator.py
exporter = ExportGenerator()
export_path = exporter.generate_export({
    "audio_file": "interview.wav",
    "video_file": "interview.mp4",
    "noise_reduction_strength": 0.5,
    "suggestions": [
        {
            "scene": "outdoor",
            "audio_path": "wind.wav",
            "accepted": True,
            "fade_in": 0.5,
            "fade_out": 0.5,
            "volume_reduction": 0.3,
        }
    ]
})
```

---

## Future Enhancements

### Track Management
- [ ] Automatic track color coding
- [ ] Track grouping (audio group, video group)
- [ ] Automation lanes for volume/pan
- [ ] Custom track icons

### Advanced Features
- [ ] Multi-track audio input
- [ ] Surround sound support
- [ ] Separate dialogue/music/effects tracks
- [ ] Stem export functionality

### Integration
- [ ] Direct REAPER plugin integration
- [ ] Real-time track preview
- [ ] Undo/redo integration
- [ ] Project template creation

---

## Summary

The separate audio and video track architecture provides:
- **Flexibility** - Independent control of each element
- **Non-destructive** - Original audio preserved
- **Professional** - Standard REAPER workflow
- **Scalable** - Easy to add more enhancement tracks
- **User-friendly** - Clear organization and naming

This design allows users to easily accept, adjust, or reject audio enhancements while maintaining full control over the final mix.
