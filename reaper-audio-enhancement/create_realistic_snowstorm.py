#!/usr/bin/env python3
"""
Create a realistic snowstorm video with animated falling snow particles.
"""

import cv2
import numpy as np
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

def create_snowstorm_video_with_particles(audio_file, video_file, duration=20, fps=30):
    """Create snowstorm video with falling snow particles."""
    print(f"Creating snowstorm video with falling snow particles...")
    
    width, height = 1280, 720
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(video_file), fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("✗ Failed to create video writer")
        return False
    
    # Create snow particles
    num_particles = 500
    particles = []
    for _ in range(num_particles):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        vx = np.random.uniform(-2, 2)  # Horizontal velocity
        vy = np.random.uniform(2, 5)   # Vertical velocity (falling)
        size = np.random.randint(2, 8)
        particles.append([x, y, vx, vy, size])
    
    particles = np.array(particles, dtype=np.float32)
    
    # Generate frames
    total_frames = int(duration * fps)
    for frame_num in range(total_frames):
        # Create dark blue background (night sky)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (20, 15, 10)  # Dark blue
        
        # Add some clouds/fog effect
        for y in range(0, height, 50):
            cv2.line(frame, (0, y), (width, y), (40, 35, 30), 1)
        
        # Update and draw particles
        for i, particle in enumerate(particles):
            x, y, vx, vy, size = particle
            
            # Update position
            x += vx
            y += vy
            
            # Wrap around edges
            if x < 0:
                x = width
            if x > width:
                x = 0
            if y > height:
                y = 0
            
            # Draw particle (white snow)
            cv2.circle(frame, (int(x), int(y)), int(size), (255, 255, 255), -1)
            
            # Update particle
            particles[i] = [x, y, vx, vy, size]
        
        # Add wind effect (horizontal streaks)
        if frame_num % 5 == 0:
            for _ in range(20):
                y = np.random.randint(0, height)
                cv2.line(frame, (0, y), (width, y), (50, 50, 50), 1)
        
        # Write frame
        out.write(frame)
        
        if (frame_num + 1) % 30 == 0:
            print(f"  Frame {frame_num + 1}/{total_frames}")
    
    out.release()
    print(f"✓ Created video: {video_file}")
    return True

def embed_audio_in_video(video_file, audio_file, output_file):
    """Embed audio into video using ffmpeg."""
    print(f"Embedding audio into video...")
    
    import subprocess
    
    cmd = [
        'ffmpeg',
        '-i', str(video_file),
        '-i', str(audio_file),
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        '-y',
        str(output_file)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Embedded audio: {output_file}")
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
    video_file_temp = sample_dir / "sample_video_temp.mp4"
    video_file = sample_dir / "sample_video.mp4"
    
    duration = 20
    
    # Create audio
    audio, sample_rate = create_snowstorm_audio(duration=duration)
    if not save_audio_wav(audio, sample_rate, str(audio_file)):
        print("✗ Failed to save audio")
        return False
    
    # Create video with particles
    if not create_snowstorm_video_with_particles(str(audio_file), str(video_file_temp), duration=duration):
        print("✗ Failed to create video")
        return False
    
    # Embed audio
    if not embed_audio_in_video(video_file_temp, audio_file, video_file):
        print("✗ Failed to embed audio")
        # Use temp file as fallback
        video_file_temp.rename(video_file)
    else:
        # Clean up temp file
        video_file_temp.unlink(missing_ok=True)
    
    print("\n✓ Realistic snowstorm video created!")
    print(f"  Audio: {audio_file} ({audio_file.stat().st_size / 1024:.1f} KB)")
    print(f"  Video: {video_file} ({video_file.stat().st_size / 1024 / 1024:.1f} MB)")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
