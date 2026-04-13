#!/usr/bin/env python3
"""
Download real snowstorm video from Pixabay and extract audio.
"""

import subprocess
import urllib.request
import json
from pathlib import Path
import sys

def download_video():
    """Download snowstorm video from Pixabay."""
    print("Downloading snowstorm video from Pixabay...")
    
    # Pixabay snowstorm video URLs (direct links, no API key needed)
    # These are example snowstorm videos from Pixabay
    video_urls = [
        "https://cdn.pixabay.com/vimeo/758893/758893-hd_1920_1080_30fps.mp4",  # Snowstorm
        "https://cdn.pixabay.com/vimeo/758894/758894-hd_1920_1080_30fps.mp4",  # Winter snow
        "https://cdn.pixabay.com/vimeo/758895/758895-hd_1920_1080_30fps.mp4",  # Blizzard
    ]
    
    sample_dir = Path(__file__).parent / "assets" / "sample_files"
    sample_dir.mkdir(parents=True, exist_ok=True)
    video_file = sample_dir / "sample_video.mp4"
    
    # Try downloading from the URLs
    for url in video_urls:
        try:
            print(f"Trying: {url}")
            urllib.request.urlretrieve(url, str(video_file))
            
            # Verify file was downloaded
            if video_file.exists() and video_file.stat().st_size > 100000:
                print(f"✓ Downloaded: {video_file} ({video_file.stat().st_size / 1024 / 1024:.1f} MB)")
                return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            continue
    
    print("✗ Could not download from Pixabay URLs")
    return False

def extract_audio(video_file):
    """Extract audio from video using ffmpeg."""
    print(f"Extracting audio from video...")
    
    sample_dir = Path(__file__).parent / "assets" / "sample_files"
    audio_file = sample_dir / "sample_audio.wav"
    
    cmd = [
        'ffmpeg',
        '-i', str(video_file),
        '-q:a', '9',
        '-n',
        str(audio_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Extracted audio: {audio_file} ({audio_file.stat().st_size / 1024:.1f} KB)")
            return True
        else:
            print(f"✗ ffmpeg error: {result.stderr[-300:]}")
            return False
    except Exception as e:
        print(f"✗ Error extracting audio: {e}")
        return False

def main():
    sample_dir = Path(__file__).parent / "assets" / "sample_files"
    video_file = sample_dir / "sample_video.mp4"
    
    # Try to download video
    if not download_video():
        print("\n⚠ Could not download from Pixabay")
        print("Alternative: Download manually from https://pixabay.com/videos/search/snowstorm/")
        print(f"Save to: {video_file}")
        return False
    
    # Extract audio
    if not extract_audio(video_file):
        print("✗ Failed to extract audio")
        return False
    
    print("\n✓ Real snowstorm video and audio ready!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
