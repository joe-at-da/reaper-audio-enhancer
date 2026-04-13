"""
Audio Library Manager - Manages audio library installation and access.
"""

from pathlib import Path
from src.utils import app_logger


class AudioLibraryManager:
    """Manage audio library for suggestions."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.library_path = self.project_root / "assets" / "audio_library"
        self.library_path.mkdir(parents=True, exist_ok=True)
    
    def is_installed(self):
        """Check if audio library is installed."""
        if not self.library_path.exists():
            return False
        
        audio_files = list(self.library_path.glob("*.wav"))
        return len(audio_files) > 0
    
    def get_library_path(self):
        """Get path to audio library."""
        return self.library_path
    
    def get_available_sounds(self):
        """Get list of available sounds in library."""
        if not self.is_installed():
            return []
        
        sounds = {}
        for audio_file in self.library_path.glob("*.wav"):
            name = audio_file.stem
            sounds[name] = str(audio_file)
        
        return sounds
    
    def get_sound(self, name):
        """Get path to specific sound file."""
        sounds = self.get_available_sounds()
        return sounds.get(name)
    
    def validate_library(self):
        """Validate audio library integrity."""
        if not self.is_installed():
            return False, "Audio library not installed"
        
        sounds = self.get_available_sounds()
        if len(sounds) == 0:
            return False, "No audio files found in library"
        
        # Check that files are valid
        for name, path in sounds.items():
            if not Path(path).exists():
                return False, f"Audio file not found: {name}"
        
        return True, f"Library OK ({len(sounds)} sounds)"
    
    def get_installation_instructions(self):
        """Get instructions for installing audio library."""
        return {
            "title": "Audio Library Installation",
            "description": "Download audio files and place them in the audio library folder",
            "library_path": str(self.library_path),
            "recommended_sources": [
                {
                    "name": "Freesound.org",
                    "url": "https://freesound.org",
                    "license": "Creative Commons",
                    "recommended_sounds": ["wind", "rain", "thunder", "snow", "ambient"]
                },
                {
                    "name": "Pixabay.com",
                    "url": "https://pixabay.com/sound-effects",
                    "license": "Free to use",
                    "recommended_sounds": ["wind", "rain", "thunder", "snow", "ambient"]
                },
                {
                    "name": "Zapsplat.com",
                    "url": "https://www.zapsplat.com",
                    "license": "Free to use",
                    "recommended_sounds": ["wind", "rain", "thunder", "snow", "ambient"]
                }
            ],
            "steps": [
                "1. Visit one of the recommended sources above",
                "2. Search for ambient sounds (wind, rain, thunder, snow, etc.)",
                "3. Download audio files in WAV format",
                "4. Place files in: " + str(self.library_path),
                "5. Restart the application",
                "6. Audio library will be automatically detected"
            ]
        }
    
    def get_status(self):
        """Get current library status."""
        if not self.is_installed():
            return {
                "installed": False,
                "sounds_count": 0,
                "status": "Not installed",
                "message": "Audio library not found. Install to enable audio suggestions."
            }
        
        sounds = self.get_available_sounds()
        valid, message = self.validate_library()
        
        return {
            "installed": True,
            "sounds_count": len(sounds),
            "status": "Installed" if valid else "Invalid",
            "message": message,
            "sounds": list(sounds.keys())
        }


# Global instance
_audio_library_manager = None

def get_audio_library_manager():
    """Get or create global audio library manager instance."""
    global _audio_library_manager
    if _audio_library_manager is None:
        _audio_library_manager = AudioLibraryManager()
    return _audio_library_manager
