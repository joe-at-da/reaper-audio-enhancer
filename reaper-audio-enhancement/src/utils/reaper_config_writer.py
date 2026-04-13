"""
REAPER Config Writer - Configure REAPER to use VLC for video playback.
"""

import platform
from pathlib import Path
from src.utils import app_logger
from src.utils.vlc_detector import get_vlc_detector


class ReaperConfigWriter:
    """Write VLC configuration to REAPER preferences."""
    
    def __init__(self):
        self.system = platform.system()
        self.reaper_config_path = self._get_reaper_config_path()
    
    def _get_reaper_config_path(self):
        """Get REAPER configuration file path."""
        if self.system == "Darwin":  # macOS
            return Path.home() / "Library" / "Application Support" / "REAPER" / "reaper.ini"
        elif self.system == "Windows":
            return Path.home() / "AppData" / "Roaming" / "REAPER" / "reaper.ini"
        elif self.system == "Linux":
            return Path.home() / ".config" / "REAPER" / "reaper.ini"
        else:
            return None
    
    def is_reaper_installed(self):
        """Check if REAPER config exists."""
        if self.reaper_config_path is None:
            return False
        return self.reaper_config_path.exists()
    
    def configure_vlc(self):
        """Configure REAPER to use VLC for video playback."""
        if not self.is_reaper_installed():
            app_logger.warning("REAPER config not found. REAPER may not be installed.")
            return False
        
        vlc_detector = get_vlc_detector()
        vlc_path = vlc_detector.get_vlc_path()
        
        if not vlc_path:
            app_logger.warning("VLC not found. Cannot configure REAPER.")
            return False
        
        try:
            # Read current config
            with open(self.reaper_config_path, 'r') as f:
                lines = f.readlines()
            
            # Find or create [Video] section
            video_section_index = None
            videoplaybackexe_index = None
            
            for i, line in enumerate(lines):
                if line.strip() == "[Video]":
                    video_section_index = i
                if video_section_index is not None and line.startswith("videoplaybackexe="):
                    videoplaybackexe_index = i
                    break
            
            # If no [Video] section, create it
            if video_section_index is None:
                # Add [Video] section before [Misc] or at end
                misc_section_index = None
                for i, line in enumerate(lines):
                    if line.strip() == "[Misc]":
                        misc_section_index = i
                        break
                
                if misc_section_index is not None:
                    lines.insert(misc_section_index, f"videoplaybackexe={vlc_path}\n")
                    lines.insert(misc_section_index, "[Video]\n")
                else:
                    lines.append("\n[Video]\n")
                    lines.append(f"videoplaybackexe={vlc_path}\n")
            else:
                # Update or add videoplaybackexe in existing [Video] section
                if videoplaybackexe_index is not None:
                    lines[videoplaybackexe_index] = f"videoplaybackexe={vlc_path}\n"
                else:
                    # Find next section or end of [Video] section
                    next_section_index = None
                    for i in range(video_section_index + 1, len(lines)):
                        if lines[i].startswith("["):
                            next_section_index = i
                            break
                    
                    if next_section_index is not None:
                        lines.insert(next_section_index, f"videoplaybackexe={vlc_path}\n")
                    else:
                        lines.append(f"videoplaybackexe={vlc_path}\n")
            
            # Write back config
            with open(self.reaper_config_path, 'w') as f:
                f.writelines(lines)
            
            app_logger.info(f"REAPER configured with VLC: {vlc_path}")
            return True
        
        except Exception as e:
            app_logger.error(f"Error configuring REAPER: {e}")
            return False
    
    def get_reaper_config_path(self):
        """Get REAPER config path."""
        return self.reaper_config_path
    
    def get_setup_instructions(self):
        """Get instructions for manual REAPER setup."""
        system = self.system
        vlc_detector = get_vlc_detector()
        vlc_path = vlc_detector.get_vlc_path()
        
        if system == "Darwin":
            return {
                "system": "macOS",
                "config_file": str(self.reaper_config_path),
                "instructions": [
                    "1. Open REAPER",
                    "2. Go to REAPER > Preferences",
                    "3. Search for 'Video'",
                    "4. Find 'Video Playback' section",
                    f"5. Set video player to: {vlc_path}",
                    "6. Click OK",
                    "7. Restart REAPER"
                ]
            }
        elif system == "Windows":
            return {
                "system": "Windows",
                "config_file": str(self.reaper_config_path),
                "instructions": [
                    "1. Open REAPER",
                    "2. Go to Options > Preferences",
                    "3. Search for 'Video'",
                    "4. Find 'Video Playback' section",
                    f"5. Set video player to: {vlc_path}",
                    "6. Click OK",
                    "7. Restart REAPER"
                ]
            }
        elif system == "Linux":
            return {
                "system": "Linux",
                "config_file": str(self.reaper_config_path),
                "instructions": [
                    "1. Open REAPER",
                    "2. Go to Options > Preferences",
                    "3. Search for 'Video'",
                    "4. Find 'Video Playback' section",
                    f"5. Set video player to: {vlc_path}",
                    "6. Click OK",
                    "7. Restart REAPER"
                ]
            }
        else:
            return {
                "system": system,
                "config_file": str(self.reaper_config_path),
                "instructions": ["Manual configuration required"]
            }


# Global instance
_reaper_config_writer = None

def get_reaper_config_writer():
    """Get or create global REAPER config writer instance."""
    global _reaper_config_writer
    if _reaper_config_writer is None:
        _reaper_config_writer = ReaperConfigWriter()
    return _reaper_config_writer
