#!/usr/bin/env python3
"""
Train scene classifier on sample videos.
This allows the app to learn scene types without hardcoding.

Usage:
    python scripts/train_scene_classifier.py

The script will look for sample videos in assets/sample_files/:
    - sample_video.mp4 (or sample_video_snow.mp4) → "snow"
    - sample_video_rain.mp4 → "rain"
    - sample_video_car.mp4 → "car"

You can add more scene types by creating sample videos with the naming pattern:
    sample_video_<scene_type>.mp4
"""

import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.video.scene_classifier import get_scene_classifier
from src.utils import app_logger


def find_sample_videos():
    """Find all sample videos in assets/sample_files/"""
    sample_dir = project_root / "assets" / "sample_files"
    
    if not sample_dir.exists():
        app_logger.error(f"Sample directory not found: {sample_dir}")
        return {}
    
    training_videos = {}
    
    # Look for sample_video_<type>.mp4 files
    for video_file in sample_dir.glob("sample_video_*.mp4"):
        # Extract scene type from filename
        # sample_video_rain.mp4 → rain
        scene_type = video_file.stem.replace("sample_video_", "")
        training_videos[scene_type] = str(video_file)
    
    # Also check for sample_video.mp4 (default/snow)
    default_video = sample_dir / "sample_video.mp4"
    if default_video.exists() and "snow" not in training_videos:
        training_videos["snow"] = str(default_video)
    
    return training_videos


def main():
    """Train scene classifier."""
    
    print("\n" + "="*60)
    print("SCENE CLASSIFIER TRAINING")
    print("="*60 + "\n")
    
    # Find sample videos
    training_videos = find_sample_videos()
    
    if not training_videos:
        print("❌ No sample videos found!")
        print("   Expected: assets/sample_files/sample_video_<type>.mp4")
        print("   Example: sample_video_rain.mp4, sample_video_car.mp4")
        return False
    
    print(f"Found {len(training_videos)} scene types:")
    for scene_type, video_path in training_videos.items():
        print(f"  - {scene_type}: {Path(video_path).name}")
    
    print("\nTraining classifier...")
    print("-" * 60)
    
    # Train classifier
    classifier = get_scene_classifier()
    success = classifier.train(training_videos)
    
    print("-" * 60)
    
    if success:
        print("\n✓ Classifier trained successfully!")
        print(f"  Trained on: {classifier.scene_types}")
        print(f"  Model saved to: {classifier.model_path}")
        print("\nThe app will now use this classifier for scene detection.")
        print("No hardcoded thresholds needed!")
        return True
    else:
        print("\n❌ Training failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
