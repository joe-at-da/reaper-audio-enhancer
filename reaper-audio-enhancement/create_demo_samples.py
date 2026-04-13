#!/usr/bin/env python3
"""
Create realistic demo samples for snowstorm scenario.
Generates snowstorm audio and creates a video with that audio.
"""

import numpy as np
import subprocess
from pathlib import Path
import sys

def create_snowstorm_audio(duration=20, sample_rate=44100):
    """Create realistic snowstorm audio using noise synthesis."""
    print(f"Creating {duration}s snowstorm audio...")
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Base wind noise (low frequency)
    wind = np.random.normal(0, 0.3, len(t))
    wind_filtered = np.convolve(wind, np.ones(1000)/1000, mode='same')
    
    # Snow falling sound (mid-high frequency)
    snow = np.random.normal(0, 0.2, len(t))
    snow_filtered = np.convolve(snow, np.ones(500)/500, mode='same')
    
    # Occasional gusts (amplitude modulation)
    gusts = 0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t)  # 0.5 Hz oscillation
    
    # Combine all components
    audio = (wind_filtered * 0.6 + snow_filtered * 0.4) * gusts
    
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.9
    
    # Convert to 16-bit PCM
    audio_int16 = np.int16(audio * 32767)
    
    return audio_int16, sample_rate

def save_audio_wav(audio, sample_rate, filename):
    """Save audio to WAV file using scipy."""
    try:
        from scipy.io import wavfile
        wavfile.write(filename, sample_rate, audio)
        print(f"✓ Saved audio: {filename}")
        return True
    except ImportError:
        print("scipy not available, using ffmpeg instead...")
        return False

def create_video_from_audio(audio_file, video_file, duration=20):
    """Create a video file from audio using ffmpeg."""
    print(f"Creating video from audio...")
    
    # Create a simple dark video with the audio
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=0x1a1a2e:s=1280x720:d={duration}',
        '-i', audio_file,
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-shortest',
        '-y',
        video_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Created video: {video_file}")
            return True
        else:
            print(f"ffmpeg error: {result.stderr[-300:]}")
    except Exception as e:
        print(f"✗ Error creating video: {e}")
    
    return False

def main():
    sample_dir = Path(__file__).parent / "assets" / "sample_files"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    audio_file = sample_dir / "sample_audio.wav"
    video_file = sample_dir / "sample_video.mp4"
    
    duration = 20  # 20 seconds
    
    # Create audio
    audio, sample_rate = create_snowstorm_audio(duration=duration)
    
    # Save audio
    if not save_audio_wav(audio, sample_rate, str(audio_file)):
        print("✗ Failed to save audio")
        return False
    
    # Create video from audio
    if not create_video_from_audio(str(audio_file), str(video_file), duration=duration):
        print("✗ Failed to create video")
        return False
    
    print("\n✓ Demo samples created successfully!")
    print(f"  Audio: {audio_file}")
    print(f"  Video: {video_file}")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
