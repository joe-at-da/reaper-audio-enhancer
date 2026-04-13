# Real Sample Files Setup Guide

**Status**: Smart file detection implemented, real sample files needed

---

## Overview

The application now includes smart file type validation. To complete the demo setup, you need to download real snowstorm audio and video files.

---

## Recommended Sample Files

### Audio File (Snowstorm)

**Option 1: Freesound - Howling Winter Storm**
- URL: https://freesound.org/people/DBlover/sounds/505999/
- Duration: ~30 seconds (perfect for demo)
- Quality: High quality winter storm ambience
- License: Creative Commons
- Download as: WAV format

**Option 2: Freesound - Snowstorm City**
- URL: https://freesound.org/people/klankbeeld/sounds/413518/
- Duration: Variable (check before download)
- Quality: Realistic snowstorm in urban setting
- License: Creative Commons

### Video File (Snowstorm)

**Option 1: Pixabay - Snow Storm Videos**
- URL: https://pixabay.com/videos/search/snow%20storm/
- Duration: 15-30 seconds
- Quality: HD/4K available
- License: Free to use
- Download as: MP4 format

**Option 2: Pixabay - Snowfall Videos**
- URL: https://pixabay.com/videos/search/snowfall/
- Duration: 15-30 seconds
- Quality: HD/4K available
- License: Free to use

---

## Installation Steps

### Step 1: Download Files

1. Go to Freesound.org and download a snowstorm audio file
2. Go to Pixabay.com and download a snowstorm video file
3. Ensure both are 15-30 seconds duration

### Step 2: Convert to Required Format

**Audio**:
- If downloaded as MP3: Keep as is (supported)
- If downloaded as OGG: Convert to WAV using Audacity or ffmpeg
- Command: `ffmpeg -i input.ogg -acodec pcm_s16le -ar 44100 output.wav`

**Video**:
- If downloaded as MP4: Keep as is (supported)
- If downloaded as WebM: Convert to MP4 using ffmpeg
- Command: `ffmpeg -i input.webm -c:v libx264 -c:a aac output.mp4`

### Step 3: Replace Sample Files

Replace the existing sample files:

```bash
# Backup originals (optional)
mv assets/sample_files/sample_audio.wav assets/sample_files/sample_audio.wav.bak
mv assets/sample_files/sample_video.mp4 assets/sample_files/sample_video.mp4.bak

# Copy new files
cp ~/Downloads/snowstorm_audio.wav assets/sample_files/sample_audio.wav
cp ~/Downloads/snowstorm_video.mp4 assets/sample_files/sample_video.mp4
```

### Step 4: Test

```bash
bash launch.sh demo
```

Expected behavior:
1. Demo loads with real snowstorm audio/video
2. Click "1. Analyze"
3. Audio analysis detects snowstorm sounds
4. Video analysis detects snowstorm scene
5. Suggestions include relevant ambient sounds (wind, snow, etc.)
6. Click "3. Export to REAPER"
7. Click "4. Import to REAPER"
8. REAPER opens with:
   - Original audio track (snowstorm audio)
   - Video track (snowstorm video visible)
   - Enhancement tracks (suggested ambient sounds)

---

## Smart File Detection

The application now validates file types when you select audio or video:

### Audio Selection
- ✓ Accepts: WAV, MP3, FLAC, OGG, etc.
- ✓ Validates using librosa library
- ✗ Rejects: Video files
- Error message: "This appears to be a video file, not audio. Please select an audio file."

### Video Selection
- ✓ Accepts: MP4, MOV, AVI, WebM, etc.
- ✓ Validates using OpenCV library
- ✗ Rejects: Audio files
- Error message: "This appears to be an audio file, not video. Please select a video file."

### Duplicate File Handling
- If user selects two audio files → Uses the last one selected
- If user selects two video files → Uses the last one selected
- If user selects audio for audio + video for video → Uses both (ignores video's audio)

---

## Troubleshooting

### "This appears to be a video file, not audio"
- You selected a video file for audio
- Solution: Click "Browse Audio" and select an actual audio file

### "This appears to be an audio file, not video"
- You selected an audio file for video
- Solution: Click "Browse Video" and select an actual video file

### File validation fails on valid file
- The file format might not be supported
- Try converting to WAV (audio) or MP4 (video)
- Check file integrity (not corrupted)

### Demo still shows noise
- The sample files haven't been replaced yet
- Follow the installation steps above
- Restart the application after replacing files

---

## File Specifications

### Ideal Audio File
- Format: WAV or MP3
- Duration: 15-30 seconds
- Sample Rate: 44100 Hz or higher
- Channels: Mono or Stereo
- Content: Clear, recognizable sounds (snowstorm, rain, traffic, etc.)

### Ideal Video File
- Format: MP4
- Duration: 15-30 seconds
- Resolution: 1080p or higher
- Frame Rate: 24-30 fps
- Codec: H.264
- Content: Clear, recognizable scenes (snowstorm, rain, traffic, etc.)

---

## Notes

- The application works with any audio/video files, not just snowstorm
- Real-world usage will use user-provided files
- Demo is just an example to showcase the tool's capabilities
- Smart file detection helps prevent user errors
- All error messages are localized (English and Ukrainian)

---

## Next Steps

1. Download real snowstorm audio and video files
2. Replace the sample files in `assets/sample_files/`
3. Test the complete workflow
4. Verify REAPER shows both audio and video tracks
5. Verify suggestions are relevant to the content

Once real sample files are in place, the demo will be much more representative of real-world usage!
