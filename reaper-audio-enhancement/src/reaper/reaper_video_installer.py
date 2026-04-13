"""
REAPER Video Installer - Automatically install and run video import script.
Handles copying ReaScript to REAPER's Scripts folder and executing it.
"""

import platform
import subprocess
from pathlib import Path
from src.utils import app_logger


class ReaperVideoInstaller:
    """Install and run video import ReaScript in REAPER."""
    
    def __init__(self):
        self.system = platform.system()
        self.reaper_scripts_path = self._get_reaper_scripts_path()
    
    def _get_reaper_scripts_path(self):
        """Get REAPER Scripts folder path."""
        if self.system == "Darwin":  # macOS
            return Path.home() / "Library" / "Application Support" / "REAPER" / "Scripts"
        elif self.system == "Windows":
            return Path.home() / "AppData" / "Roaming" / "REAPER" / "Scripts"
        elif self.system == "Linux":
            return Path.home() / ".config" / "REAPER" / "Scripts"
        else:
            return None
    
    def install_video_script(self):
        """Install video import script to REAPER Scripts folder."""
        if not self.reaper_scripts_path:
            app_logger.error(f"Unknown platform: {self.system}")
            return False
        
        try:
            # Create Scripts folder if it doesn't exist
            self.reaper_scripts_path.mkdir(parents=True, exist_ok=True)
            
            # Get the script source
            script_source = Path(__file__).parent.parent.parent / "scripts" / "add_video_to_reaper.py"
            
            if not script_source.exists():
                app_logger.error(f"Script not found: {script_source}")
                return False
            
            # Copy script to REAPER Scripts folder
            script_dest = self.reaper_scripts_path / "add_video_to_reaper.py"
            
            with open(script_source, 'r') as f:
                script_content = f.read()
            
            with open(script_dest, 'w') as f:
                f.write(script_content)
            
            app_logger.info(f"Video script installed: {script_dest}")
            return True
        
        except Exception as e:
            app_logger.error(f"Error installing video script: {e}")
            return False
    
    def run_video_script_via_osc(self, osc_host="127.0.0.1", osc_port=9000):
        """Run video script via REAPER OSC."""
        try:
            import socket
            import struct
            
            # Create OSC message to run the script
            # Format: /action/40886 (Run script)
            # We'll use a different approach - send command to execute script
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # OSC message format for running action
            # This is complex - we'll use a simpler approach
            
            app_logger.debug("OSC method requires complex message formatting")
            return False
        
        except Exception as e:
            app_logger.error(f"Error running script via OSC: {e}")
            return False
    
    def run_video_script_via_command_line(self, project_path):
        """Run video script by opening REAPER with command line."""
        try:
            # This approach opens REAPER with a script parameter
            # REAPER will execute the script on startup
            
            if self.system == "Darwin":
                # macOS: Use open command with script parameter
                cmd = [
                    "open",
                    "-a", "REAPER",
                    "--args",
                    f"--script={self.reaper_scripts_path}/add_video_to_reaper.py",
                    str(project_path)
                ]
            elif self.system == "Windows":
                cmd = [
                    "reaper.exe",
                    f"/script={self.reaper_scripts_path}/add_video_to_reaper.py",
                    str(project_path)
                ]
            elif self.system == "Linux":
                cmd = [
                    "reaper",
                    f"--script={self.reaper_scripts_path}/add_video_to_reaper.py",
                    str(project_path)
                ]
            else:
                return False
            
            subprocess.Popen(cmd)
            app_logger.info("Video script executed via command line")
            return True
        
        except Exception as e:
            app_logger.error(f"Error running script via command line: {e}")
            return False
    
    def get_script_path(self):
        """Get the full path to the installed video script."""
        return self.reaper_scripts_path / "add_video_to_reaper.py"
    
    def create_reaper_action(self):
        """
        Note: REAPER action registration is complex and requires manual setup.
        Instead, we provide the script path for the user to create an action manually.
        """
        script_path = self.get_script_path()
        app_logger.info(f"Video script available at: {script_path}")
        app_logger.info("User can create a custom action in REAPER pointing to this script")
        return True
    
    def get_setup_instructions(self):
        """Get instructions for manual setup."""
        return {
            "method": "manual",
            "steps": [
                "1. In REAPER: Actions > Show action list",
                "2. New... > Create new action",
                f"3. Paste content from: {Path(__file__).parent.parent.parent / 'scripts' / 'add_video_to_reaper.py'}",
                "4. Run the action",
                "5. Video will be added to your project"
            ]
        }


# Global instance
_reaper_video_installer = None

def get_reaper_video_installer():
    """Get or create global REAPER video installer instance."""
    global _reaper_video_installer
    if _reaper_video_installer is None:
        _reaper_video_installer = ReaperVideoInstaller()
    return _reaper_video_installer
