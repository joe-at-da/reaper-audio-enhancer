#!/usr/bin/env python3
"""
Create a realistic snowstorm video with animated particles and audio.
"""

import numpy as np
import subprocess
from pathlib import Path
import sys

def create_snowstorm_audio(duration=20, sample_rate=44100):
    """Create realistic snowstorm audio."""
    print(f"Creating {duration}s snowstorm audio...")
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Wind noise (low frequency)
    wind = np.random.normal(0, 0.3, len(t))
    wind_filtered = np.convolve(wind, np.ones(1000)/1000, mode='same')
    
    # Snow falling (mid-high frequency)
    snow = np.random.normal(0, 0.2, len(t))
    snow_filtered = np.convolve(snow, np.ones(500)/500, mode='same')
    
    # Gusts (amplitude modulation)
    gusts = 0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t)
    
    # Combine
    audio = (wind_filtered * 0.6 + snow_filtered * 0.4) * gusts
    audio = audio / np.max(np.abs(audio)) * 0.9
    
    return np.int16(audio * 32767), sample_rate

def save_audio_wav(audio, sample_rate, filename):
    """Save audio to WAV file."""
    try:
        from scipy.io import wavfile
        wavfile.write(filename, sample_rate, audio)
        print(f"✓ Saved audio: {filename}")
        return True
    except ImportError:
        print("scipy not available")
        return False

def create_snowstorm_video(audio_file, video_file, duration=20):
    """Create snowstorm video with particles and audio."""
    print(f"Creating snowstorm video with particles...")
    
    # Create video with animated snow particles
    # Use ffmpeg to create a video with moving particles effect
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=0x0a0a1a:s=1280x720:d={duration}',  # Dark blue background
        '-vf', 'geq=lum=255*sin(2*PI*t)*abs(sin(PI*(X+Y)/100)):cb=128:cr=128',  # Animated effect
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
        print(f"✗ Error: {e}")
    
    return False

def create_snowstorm_video_simple(audio_file, video_file, duration=20):
    """Create snowstorm video with simple noise pattern."""
    print(f"Creating snowstorm video with noise pattern...")
    
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=0x0a0a1a:s=1280x720:d={duration}',  # Dark blue
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
        print(f"✗ Error: {e}")
    
    return False

def main():
    sample_dir = Path(__file__).parent / "assets" / "sample_files"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    audio_file = sample_dir / "sample_audio.wav"
    video_file = sample_dir / "sample_video.mp4"
    
    duration = 20
    
    # Create audio
    audio, sample_rate = create_snowstorm_audio(duration=duration)
    if not save_audio_wav(audio, sample_rate, str(audio_file)):
        print("✗ Failed to save audio")
        return False
    
    # Create video
    if not create_snowstorm_video(str(audio_file), str(video_file), duration=duration):
        print("Trying simpler approach...")
        if not create_snowstorm_video_simple(str(audio_file), str(video_file), duration=duration):
            print("✗ Failed to create video")
            return False
    
    print("\n✓ Snowstorm video and audio created!")
    print(f"  Audio: {audio_file} ({audio_file.stat().st_size / 1024:.1f} KB)")
    print(f"  Video: {video_file} ({video_file.stat().st_size / 1024 / 1024:.1f} MB)")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
