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
        Deduplicates suggestions by (audio_file, start_time) to avoid duplicate tracks.
        """
        try:
            suggestions = []
            available_files = self.get_available_audio_files()
            
            for scene_type, confidence in detected_scenes:
                if scene_type in self.scene_audio_map:
                    audio_files = available_files.get(scene_type, [])
                    # For each scene, suggest only the best audio file (highest confidence)
                    # instead of all available files for that scene type
                    if audio_files:
                        # Pick the first (best) audio file for this scene
                        audio_file = audio_files[0]
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
            
            # Deduplicate by (audio_file, scene_type) - keep highest confidence
            deduplicated = self._deduplicate_suggestions(suggestions)
            deduplicated.sort(key=lambda x: x["priority"], reverse=True)
            
            app_logger.info(f"Generated {len(deduplicated)} audio suggestions (after deduplication)")
            return deduplicated
        except Exception as e:
            app_logger.error(f"Error suggesting audio: {e}")
            return []
    
    def _deduplicate_suggestions(self, suggestions):
        """
        Remove duplicate suggestions by (audio_file, scene_type).
        Keeps the suggestion with highest confidence.
        """
        try:
            seen = {}
            deduplicated = []
            
            for suggestion in suggestions:
                key = (suggestion["audio_file"], suggestion["scene"])
                
                if key not in seen:
                    seen[key] = suggestion
                    deduplicated.append(suggestion)
                else:
                    # Keep the one with higher confidence
                    if suggestion["confidence"] > seen[key]["confidence"]:
                        # Replace with higher confidence version
                        deduplicated.remove(seen[key])
                        seen[key] = suggestion
                        deduplicated.append(suggestion)
            
            return deduplicated
        except Exception as e:
            app_logger.error(f"Error deduplicating suggestions: {e}")
            return suggestions
    
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
