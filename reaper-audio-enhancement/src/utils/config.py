import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / ".config"
        self.config_file = self.config_dir / "settings.json"
        self.audio_library_path = self.project_root / "assets" / "audio_library"
        self.sample_files_path = self.project_root / "assets" / "sample_files"
        
        self.config_dir.mkdir(exist_ok=True)
        self.audio_library_path.mkdir(parents=True, exist_ok=True)
        self.sample_files_path.mkdir(parents=True, exist_ok=True)
        
        self.defaults = {
            "reaper_path": "",
            "osc_host": "127.0.0.1",
            "osc_port": 9000,
            "noise_reduction_strength": 0.5,
            "fade_duration": 0.5,
            "audio_library_path": str(self.audio_library_path),
            "sample_files_path": str(self.sample_files_path),
        }
        
        self.settings = self.load_settings()
    
    def load_settings(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return self.defaults.copy()
        return self.defaults.copy()
    
    def save_settings(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

config = Config()
