#!/usr/bin/env python3
"""
MVP Test Script - Verify all core functionality
"""

import sys
from pathlib import Path
import numpy as np
import librosa
import soundfile as sf

from src.audio import NoiseDetector, NoiseReducer, AudioSuggester
from src.video import FrameExtractor, SceneDetector
from src.reaper import ExportGenerator
from src.utils import config, app_logger

def test_audio_processing():
    """Test audio processing pipeline."""
    print("\n" + "="*60)
    print("Testing Audio Processing Pipeline")
    print("="*60)
    
    audio_file = Path(__file__).parent / "assets" / "sample_files" / "sample_audio.wav"
    
    if not audio_file.exists():
        print(f"✗ Sample audio not found: {audio_file}")
        return False
    
    try:
        detector = NoiseDetector()
        print("✓ NoiseDetector initialized")
        
        analysis = detector.analyze_audio(str(audio_file))
        if analysis:
            print(f"✓ Audio analysis complete: {analysis['duration']:.2f}s")
            print(f"  - Mean RMS: {analysis['mean_rms']:.4f}")
            print(f"  - Std RMS: {analysis['std_rms']:.4f}")
        else:
            print("✗ Audio analysis failed")
            return False
        
        reducer = NoiseReducer()
        print("✓ NoiseReducer initialized")
        
        y, sr = librosa.load(str(audio_file), sr=22050)
        noise_profile = detector.detect_noise_profile(y, duration=1.0)
        y_reduced = reducer.spectral_subtraction(y, noise_profile, strength=0.5)
        print(f"✓ Spectral subtraction applied: {len(y_reduced)} samples")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_video_analysis():
    """Test video analysis pipeline."""
    print("\n" + "="*60)
    print("Testing Video Analysis Pipeline")
    print("="*60)
    
    video_file = Path(__file__).parent / "assets" / "sample_files" / "sample_video.mp4"
    
    if not video_file.exists():
        print(f"✗ Sample video not found: {video_file}")
        return False
    
    try:
        extractor = FrameExtractor()
        print("✓ FrameExtractor initialized")
        
        if extractor.load_video(str(video_file)):
            print(f"✓ Video loaded: {extractor.total_frames} frames, {extractor.fps} fps")
        else:
            print("✗ Failed to load video")
            return False
        
        detector = SceneDetector()
        print("✓ SceneDetector initialized")
        
        scenes = detector.detect_scenes(str(video_file), interval=2.0)
        if scenes:
            print(f"✓ Scene detection complete: {len(scenes)} scenes detected")
            for scene in scenes[:3]:
                print(f"  - {scene['timestamp']:.1f}s: {scene['scene_type']} ({scene['confidence']:.0%})")
        else:
            print("✗ Scene detection failed")
            return False
        
        dominant = detector.get_dominant_scene(scenes)
        if dominant:
            print(f"✓ Dominant scene: {dominant['scene_type']} ({dominant['confidence']:.0%})")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_audio_suggestions():
    """Test audio suggestion engine."""
    print("\n" + "="*60)
    print("Testing Audio Suggestion Engine")
    print("="*60)
    
    try:
        suggester = AudioSuggester()
        print("✓ AudioSuggester initialized")
        
        available = suggester.get_available_audio_files()
        total_files = sum(len(v) for v in available.values())
        print(f"✓ Audio library loaded: {total_files} files")
        for scene, files in available.items():
            if files:
                print(f"  - {scene}: {len(files)} file(s)")
        
        detected_scenes = [("storm", 0.8), ("outdoor", 0.6)]
        suggestions = suggester.suggest_audio_for_scene(detected_scenes)
        if suggestions:
            print(f"✓ Generated {len(suggestions)} suggestions")
            for i, sugg in enumerate(suggestions[:3]):
                print(f"  - {sugg['scene']}: {sugg['audio_file']} ({sugg['confidence']:.0%})")
        else:
            print("⚠ No suggestions generated (audio library may be empty)")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_export():
    """Test REAPER export functionality."""
    print("\n" + "="*60)
    print("Testing REAPER Export")
    print("="*60)
    
    try:
        exporter = ExportGenerator()
        print("✓ ExportGenerator initialized")
        
        project_data = {
            "audio_file": "test_audio.wav",
            "video_file": "test_video.mp4",
            "noise_reduction_strength": 0.5,
            "suggestions": [
                {
                    "scene": "storm",
                    "audio_path": "/path/to/wind.wav",
                    "accepted": True,
                    "start_time": 0,
                    "duration": 10,
                    "fade_in": 0.5,
                    "fade_out": 0.5,
                    "volume_reduction": 0.3,
                }
            ]
        }
        
        export_path = exporter.generate_export(project_data)
        if export_path and export_path.exists():
            print(f"✓ Export generated: {export_path.name}")
            print(f"  - File size: {export_path.stat().st_size} bytes")
        else:
            print("✗ Export generation failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_configuration():
    """Test configuration system."""
    print("\n" + "="*60)
    print("Testing Configuration System")
    print("="*60)
    
    try:
        print("✓ Config loaded")
        print(f"  - OSC Host: {config.get('osc_host')}")
        print(f"  - OSC Port: {config.get('osc_port')}")
        print(f"  - Noise Reduction Strength: {config.get('noise_reduction_strength')}")
        
        config.set("test_key", "test_value")
        if config.get("test_key") == "test_value":
            print("✓ Config read/write working")
        else:
            print("✗ Config read/write failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("REAPER Audio Enhancement MVP - Test Suite")
    print("="*60)
    
    results = {
        "Audio Processing": test_audio_processing(),
        "Video Analysis": test_video_analysis(),
        "Audio Suggestions": test_audio_suggestions(),
        "REAPER Export": test_export(),
        "Configuration": test_configuration(),
    }
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All MVP tests passed! Application is ready for use.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
