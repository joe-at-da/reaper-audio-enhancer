import os
from pathlib import Path
from src.utils import app_logger, config

class AudioSuggester:
    def __init__(self):
        self.audio_library_path = Path(config.get("audio_library_path"))
        
        self.scene_audio_map = {
            "storm": ["thunder.wav", "rain.wav", "wind.wav"],
            "car_ride": ["car_engine.wav", "wind.wav"],
            "outdoor": ["wind.wav", "ambient_nature.wav"],
            "indoor": ["ambient_nature.wav"],
            "traffic": ["car_engine.wav"],
        }
    
    def get_available_audio_files(self):
        """
        Get list of available audio files in library.
        """
        try:
            if not self.audio_library_path.exists():
                app_logger.warning(f"Audio library path does not exist: {self.audio_library_path}")
                return {}
            
            available = {}
            for scene, files in self.scene_audio_map.items():
                available[scene] = []
                for filename in files:
                    filepath = self.audio_library_path / filename
                    if filepath.exists():
                        available[scene].append({
                            "name": filename,
                            "path": str(filepath),
                            "size": filepath.stat().st_size,
                        })
            
            app_logger.info(f"Found {sum(len(v) for v in available.values())} audio files")
            return available
        except Exception as e:
            app_logger.error(f"Error getting audio files: {e}")
            return {}
    
    def suggest_audio_for_scene(self, detected_scenes):
        """
        Suggest audio files based on detected scenes.
        detected_scenes: list of (scene_type, confidence) tuples
        """
        try:
            suggestions = []
            available_files = self.get_available_audio_files()
            
            for scene_type, confidence in detected_scenes:
                if scene_type in self.scene_audio_map:
                    audio_files = available_files.get(scene_type, [])
                    for audio_file in audio_files:
                        suggestions.append({
                            "scene": scene_type,
                            "confidence": confidence,
                            "audio_file": audio_file["name"],
                            "audio_path": audio_file["path"],
                            "fade_in": 0.5,
                            "fade_out": 0.5,
                            "volume_reduction": 0.3,
                            "priority": confidence,
                        })
            
            suggestions.sort(key=lambda x: x["priority"], reverse=True)
            
            app_logger.info(f"Generated {len(suggestions)} audio suggestions")
            return suggestions
        except Exception as e:
            app_logger.error(f"Error suggesting audio: {e}")
            return []
    
    def create_fade_envelope(self, duration, fade_in=0.5, fade_out=0.5, sr=22050):
        """
        Create fade in/out envelope for audio.
        """
        try:
            total_samples = int(duration * sr)
            fade_in_samples = int(fade_in * sr)
            fade_out_samples = int(fade_out * sr)
            
            envelope = np.ones(total_samples)
            
            if fade_in_samples > 0:
                envelope[:fade_in_samples] = np.linspace(0, 1, fade_in_samples)
            
            if fade_out_samples > 0:
                envelope[-fade_out_samples:] = np.linspace(1, 0, fade_out_samples)
            
            return envelope
        except Exception as e:
            app_logger.error(f"Error creating fade envelope: {e}")
            return None
