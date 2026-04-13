"""
VLC Detector - Find VLC installation on the system.
"""

import subprocess
import platform
from pathlib import Path
from src.utils import app_logger


class VLCDetector:
    """Detect VLC installation on the system."""
    
    def __init__(self):
        self.system = platform.system()
        self.vlc_path = None
    
    def find_vlc(self):
        """Find VLC installation on the system."""
        if self.system == "Darwin":  # macOS
            return self._find_vlc_macos()
        elif self.system == "Windows":
            return self._find_vlc_windows()
        elif self.system == "Linux":
            return self._find_vlc_linux()
        else:
            app_logger.warning(f"Unsupported system: {self.system}")
            return None
    
    def _find_vlc_macos(self):
        """Find VLC on macOS."""
        # Check common macOS locations
        paths = [
            Path("/Applications/VLC.app/Contents/MacOS/VLC"),
            Path("/usr/local/bin/vlc"),
            Path("/opt/homebrew/bin/vlc"),
        ]
        
        for path in paths:
            if path.exists():
                self.vlc_path = str(path)
                app_logger.info(f"Found VLC on macOS: {self.vlc_path}")
                return self.vlc_path
        
        # Try which command
        try:
            result = subprocess.run(["which", "vlc"], capture_output=True, text=True)
            if result.returncode == 0:
                self.vlc_path = result.stdout.strip()
                app_logger.info(f"Found VLC via which: {self.vlc_path}")
                return self.vlc_path
        except Exception as e:
            app_logger.debug(f"which vlc failed: {e}")
        
        return None
    
    def _find_vlc_windows(self):
        """Find VLC on Windows."""
        paths = [
            Path("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"),
            Path("C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"),
            Path(f"{Path.home()}\\AppData\\Local\\VLC\\vlc.exe"),
        ]
        
        for path in paths:
            if path.exists():
                self.vlc_path = str(path)
                app_logger.info(f"Found VLC on Windows: {self.vlc_path}")
                return self.vlc_path
        
        # Try where command
        try:
            result = subprocess.run(["where", "vlc"], capture_output=True, text=True)
            if result.returncode == 0:
                self.vlc_path = result.stdout.strip().split('\n')[0]
                app_logger.info(f"Found VLC via where: {self.vlc_path}")
                return self.vlc_path
        except Exception as e:
            app_logger.debug(f"where vlc failed: {e}")
        
        return None
    
    def _find_vlc_linux(self):
        """Find VLC on Linux."""
        # Try which command
        try:
            result = subprocess.run(["which", "vlc"], capture_output=True, text=True)
            if result.returncode == 0:
                self.vlc_path = result.stdout.strip()
                app_logger.info(f"Found VLC on Linux: {self.vlc_path}")
                return self.vlc_path
        except Exception as e:
            app_logger.debug(f"which vlc failed: {e}")
        
        # Check common Linux paths
        paths = [
            Path("/usr/bin/vlc"),
            Path("/usr/local/bin/vlc"),
            Path("/snap/bin/vlc"),
        ]
        
        for path in paths:
            if path.exists():
                self.vlc_path = str(path)
                app_logger.info(f"Found VLC on Linux: {self.vlc_path}")
                return self.vlc_path
        
        return None
    
    def is_installed(self):
        """Check if VLC is installed."""
        if self.vlc_path is None:
            self.find_vlc()
        return self.vlc_path is not None
    
    def get_vlc_path(self):
        """Get VLC path."""
        if self.vlc_path is None:
            self.find_vlc()
        return self.vlc_path
    
    def get_installation_url(self):
        """Get VLC download URL."""
        return "https://www.videolan.org/vlc/"
    
    def get_installation_instructions(self):
        """Get VLC installation instructions."""
        system = self.system
        
        if system == "Darwin":
            return {
                "system": "macOS",
                "url": "https://www.videolan.org/vlc/download-macos.html",
                "instructions": [
                    "1. Visit https://www.videolan.org/vlc/download-macos.html",
                    "2. Download VLC for macOS",
                    "3. Open the .dmg file",
                    "4. Drag VLC to Applications folder",
                    "5. Restart REAPER",
                    "6. REAPER will auto-detect VLC"
                ]
            }
        elif system == "Windows":
            return {
                "system": "Windows",
                "url": "https://www.videolan.org/vlc/download-windows.html",
                "instructions": [
                    "1. Visit https://www.videolan.org/vlc/download-windows.html",
                    "2. Download VLC installer",
                    "3. Run the installer",
                    "4. Follow installation wizard",
                    "5. Restart REAPER",
                    "6. REAPER will auto-detect VLC"
                ]
            }
        elif system == "Linux":
            return {
                "system": "Linux",
                "url": "https://www.videolan.org/vlc/download-linux.html",
                "instructions": [
                    "1. Ubuntu/Debian: sudo apt-get install vlc",
                    "2. Fedora/RHEL: sudo dnf install vlc",
                    "3. Arch: sudo pacman -S vlc",
                    "4. Or visit https://www.videolan.org/vlc/download-linux.html",
                    "5. Restart REAPER",
                    "6. REAPER will auto-detect VLC"
                ]
            }
        else:
            return {
                "system": system,
                "url": "https://www.videolan.org/vlc/",
                "instructions": [
                    "1. Visit https://www.videolan.org/vlc/",
                    "2. Download VLC for your system",
                    "3. Install VLC",
                    "4. Restart REAPER",
                    "5. REAPER will auto-detect VLC"
                ]
            }


# Global instance
_vlc_detector = None

def get_vlc_detector():
    """Get or create global VLC detector instance."""
    global _vlc_detector
    if _vlc_detector is None:
        _vlc_detector = VLCDetector()
    return _vlc_detector
