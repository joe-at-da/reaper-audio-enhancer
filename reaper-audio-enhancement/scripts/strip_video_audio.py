#!/usr/bin/env python3
"""
Strip audio from video files to create video-only versions.
This ensures that when videos are added to REAPER, they don't have embedded audio.

Usage:
    python scripts/strip_video_audio.py
"""

import subprocess
import sys
from pathlib import Path

def strip_audio_from_video(input_video, output_video):
    """
    Strip audio from a video file using ffmpeg.
    
    Args:
        input_video: Path to input video file
        output_video: Path to output video file (without audio)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Use ffmpeg to copy video stream without audio
        cmd = [
            'ffmpeg',
            '-i', str(input_video),
            '-c:v', 'copy',  # Copy video codec (no re-encoding)
            '-an',  # No audio
            '-y',  # Overwrite output file
            str(output_video)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✓ Stripped audio from: {input_video.name}")
            print(f"  Output: {output_video.name}")
            return True
        else:
            print(f"✗ Failed to strip audio from: {input_video.name}")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error processing {input_video.name}: {e}")
        return False

def main():
    """Strip audio from all sample video files."""
    
    print("\n" + "="*60)
    print("STRIP AUDIO FROM VIDEO FILES")
    print("="*60 + "\n")
    
    project_root = Path(__file__).parent.parent
    sample_dir = project_root / "assets" / "sample_files"
    
    if not sample_dir.exists():
        print(f"✗ Sample directory not found: {sample_dir}")
        return False
    
    # Find all video files
    video_files = [
        "sample_video.mp4",
        "sample_video_car.mp4",
        "sample_video_rain.mp4",
    ]
    
    success_count = 0
    
    for video_name in video_files:
        input_path = sample_dir / video_name
        
        if not input_path.exists():
            print(f"⊘ Skipping (not found): {video_name}")
            continue
        
        # Create output filename with _no_audio suffix
        output_name = video_name.replace(".mp4", "_no_audio.mp4")
        output_path = sample_dir / output_name
        
        if output_path.exists():
            print(f"⊘ Skipping (already exists): {output_name}")
            continue
        
        print(f"\nProcessing: {video_name}")
        if strip_audio_from_video(input_path, output_path):
            success_count += 1
    
    print("\n" + "="*60)
    if success_count > 0:
        print(f"✓ Successfully processed {success_count} video file(s)")
        print("\nNext steps:")
        print("1. Update demo_files in src/gui/main_window.py to use *_no_audio.mp4 files")
        print("2. Or rename the original files and keep the no_audio versions")
        return True
    else:
        print("✗ No videos were processed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
