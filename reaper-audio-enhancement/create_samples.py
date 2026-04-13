#!/usr/bin/env python3

import numpy as np
import soundfile as sf
import cv2
from pathlib import Path

def create_sample_audio():
    """Create sample audio with realistic speech and wind noise."""
    sr = 22050
    duration = 10
    t = np.linspace(0, duration, int(sr * duration))
    
    # Create a more realistic audio signal (simulated speech)
    # Multiple frequency components to simulate speech
    speech = 0.2 * np.sin(2 * np.pi * 200 * t)  # Fundamental
    speech += 0.15 * np.sin(2 * np.pi * 400 * t)  # Harmonic
    speech += 0.1 * np.sin(2 * np.pi * 800 * t)  # Harmonic
    speech += 0.08 * np.sin(2 * np.pi * 1600 * t)  # Harmonic
    
    # Add amplitude modulation to simulate speech patterns
    envelope = 0.5 * (1 + np.sin(2 * np.pi * 2 * t))  # 2 Hz modulation
    speech = speech * envelope
    
    # Add wind noise (low frequency noise with emphasis)
    wind_noise = 0.15 * np.random.randn(len(t))
    # Filter wind noise to emphasize low frequencies
    wind_noise += 0.1 * np.sin(2 * np.pi * 80 * t)
    wind_noise += 0.08 * np.sin(2 * np.pi * 120 * t)
    
    # Add some background hum (60 Hz electrical noise)
    hum = 0.05 * np.sin(2 * np.pi * 60 * t)
    
    # Combine all components
    audio = speech + wind_noise + hum
    audio = np.clip(audio, -1, 1)
    
    output_path = Path(__file__).parent / "assets" / "sample_files" / "sample_audio.wav"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    sf.write(output_path, audio, sr)
    print(f"✓ Sample audio created: {output_path}")
    print(f"  - Duration: {duration}s")
    print(f"  - Content: Speech + wind noise + electrical hum")
    return output_path

def create_sample_video():
    """Create sample video with outdoor/storm scene transitions."""
    width, height = 640, 480
    fps = 30
    duration = 10
    total_frames = int(fps * duration)
    
    output_path = Path(__file__).parent / "assets" / "sample_files" / "sample_video.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    for frame_num in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        progress = frame_num / total_frames
        
        # Create scene transitions with more visual content
        if progress < 0.3:
            # Clear outdoor scene (blue sky)
            color_bg = (200, 150, 50)  # Sky blue
            text = "Outdoor - Clear"
            scene_type = "outdoor"
        elif progress < 0.6:
            # Transition to storm
            color_bg = (100, 100, 120)  # Gray sky
            text = "Storm Approaching"
            scene_type = "storm"
        else:
            # Heavy storm
            color_bg = (40, 40, 80)  # Dark sky
            text = "Heavy Storm"
            scene_type = "storm"
        
        # Fill background
        frame[:] = color_bg
        
        # Add some visual elements (simulate trees/landscape)
        if progress < 0.3:
            # Draw trees for outdoor scene
            cv2.rectangle(frame, (50, 300), (100, 480), (34, 139, 34), -1)  # Green tree
            cv2.rectangle(frame, (500, 280), (550, 480), (34, 139, 34), -1)  # Green tree
            cv2.circle(frame, (75, 250), 40, (34, 139, 34), -1)  # Tree top
            cv2.circle(frame, (525, 240), 40, (34, 139, 34), -1)  # Tree top
        else:
            # Add rain/storm effects
            for i in range(0, width, 20):
                cv2.line(frame, (i, 0), (i + 10, height), (150, 150, 150), 2)  # Rain lines
        
        # Add text
        cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Scene: {scene_type}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1)
        cv2.putText(frame, f"Time: {progress*10:.1f}s / 10s", (50, 450), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 1)
        
        out.write(frame)
    
    out.release()
    print(f"✓ Sample video created: {output_path}")
    print(f"  - Duration: {duration}s")
    print(f"  - Content: Outdoor scene → Storm transition")
    return output_path

def create_ambient_sounds():
    """Create sample ambient sound files with realistic characteristics."""
    sr = 22050
    duration = 5
    t = np.linspace(0, duration, int(sr * duration))
    
    ambient_sounds = {}
    
    # Wind sound - low frequency with noise
    wind = 0.2 * np.sin(2 * np.pi * 60 * t) + 0.25 * np.random.randn(len(t))
    wind += 0.15 * np.sin(2 * np.pi * 100 * t)
    ambient_sounds["wind.wav"] = wind
    
    # Rain sound - white noise with some structure
    rain = 0.3 * np.random.randn(len(t))
    rain += 0.1 * np.sin(2 * np.pi * 150 * t)
    rain += 0.08 * np.sin(2 * np.pi * 300 * t)
    ambient_sounds["rain.wav"] = rain
    
    # Thunder sound - low frequency burst
    thunder = 0.4 * np.sin(2 * np.pi * 50 * t) + 0.3 * np.random.randn(len(t))
    thunder += 0.2 * np.sin(2 * np.pi * 100 * t)
    ambient_sounds["thunder.wav"] = thunder
    
    # Car engine - mid frequency with harmonics
    car = 0.3 * np.sin(2 * np.pi * 120 * t) + 0.2 * np.sin(2 * np.pi * 240 * t)
    car += 0.15 * np.sin(2 * np.pi * 360 * t) + 0.1 * np.random.randn(len(t))
    ambient_sounds["car_engine.wav"] = car
    
    # Nature ambience - multiple frequency components
    nature = 0.15 * np.sin(2 * np.pi * 100 * t) + 0.12 * np.sin(2 * np.pi * 200 * t)
    nature += 0.1 * np.sin(2 * np.pi * 400 * t) + 0.08 * np.random.randn(len(t))
    ambient_sounds["ambient_nature.wav"] = nature
    
    output_dir = Path(__file__).parent / "assets" / "audio_library"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    descriptions = {
        "wind.wav": "Wind ambience (low frequency)",
        "rain.wav": "Rain sound (white noise + structure)",
        "thunder.wav": "Thunder (deep bass burst)",
        "car_engine.wav": "Car engine (mid frequency harmonics)",
        "ambient_nature.wav": "Nature ambience (birds, wind, etc)",
    }
    
    for filename, audio in ambient_sounds.items():
        audio = np.clip(audio, -1, 1)
        output_path = output_dir / filename
        sf.write(output_path, audio, sr)
        print(f"✓ Ambient sound created: {output_path}")
        print(f"  - {descriptions[filename]}")

if __name__ == "__main__":
    print("Creating sample files...")
    print()
    
    try:
        create_sample_audio()
        create_sample_video()
        create_ambient_sounds()
        print()
        print("✓ All sample files created successfully!")
    except Exception as e:
        print(f"✗ Error creating samples: {e}")
        exit(1)
