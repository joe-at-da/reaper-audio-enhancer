import json
from pathlib import Path
from src.utils import app_logger
from src.reaper.reaper_project_generator import ReaperProjectGenerator


class ReaperImporter:
    """
    Core importer logic for REAPER.
    Handles JSON parsing, validation, and orchestration of track creation.
    """
    
    def __init__(self):
        self.export_dir = Path.home() / ".reaper_audio_enhancement" / "exports"
        self.export_data = None
        self.import_method = None
    
    def import_json(self, json_file):
        """
        Parse and validate JSON file.
        Returns True if valid, False otherwise.
        """
        try:
            json_path = Path(json_file)
            
            if not json_path.exists():
                app_logger.error(f"JSON file not found: {json_file}")
                return False
            
            with open(json_path, 'r') as f:
                self.export_data = json.load(f)
            
            if not self._validate_export_data():
                return False
            
            app_logger.info(f"Successfully loaded export data from {json_file}")
            return True
        except json.JSONDecodeError as e:
            app_logger.error(f"Invalid JSON file: {e}")
            return False
        except Exception as e:
            app_logger.error(f"Error loading JSON: {e}")
            return False
    
    def _validate_export_data(self):
        """
        Validate that export data has required structure.
        """
        if not self.export_data:
            app_logger.error("No export data loaded")
            return False
        
        required_keys = ["audio_track", "enhancement_tracks"]
        for key in required_keys:
            if key not in self.export_data:
                app_logger.error(f"Missing required key in export data: {key}")
                return False
        
        return True
    
    def validate_audio_files(self):
        """
        Check if all referenced audio files exist.
        Returns dict with status for each file.
        """
        validation = {
            "audio_file": False,
            "video_file": False,
            "enhancement_files": {}
        }
        
        try:
            # Check audio file
            audio_file = self.export_data.get("audio_track", {}).get("file")
            if audio_file:
                audio_path = Path(audio_file)
                validation["audio_file"] = audio_path.exists()
                if not validation["audio_file"]:
                    app_logger.warning(f"Audio file not found: {audio_file}")
            
            # Check video file
            video_file = self.export_data.get("video_track", {}).get("file")
            if video_file:
                video_path = Path(video_file)
                validation["video_file"] = video_path.exists()
                if not validation["video_file"]:
                    app_logger.warning(f"Video file not found: {video_file}")
            
            # Check enhancement files
            for track in self.export_data.get("enhancement_tracks", []):
                file_path = track.get("file")
                if file_path:
                    path = Path(file_path)
                    exists = path.exists()
                    validation["enhancement_files"][file_path] = exists
                    if not exists:
                        app_logger.warning(f"Enhancement file not found: {file_path}")
            
            return validation
        except Exception as e:
            app_logger.error(f"Error validating audio files: {e}")
            return validation
    
    def get_import_method(self):
        """
        Determine best import method available.
        Returns: "osc", "reascript", or None
        """
        try:
            from src.reaper.osc_importer import OSCImporter
            osc = OSCImporter()
            if osc.connect():
                app_logger.info("OSC connection available")
                self.import_method = "osc"
                return "osc"
        except Exception as e:
            app_logger.debug(f"OSC not available: {e}")
        
        app_logger.info("OSC not available, will use ReaScript")
        self.import_method = "reascript"
        return "reascript"
    
    def get_export_data(self):
        """
        Get the loaded export data.
        """
        return self.export_data
    
    def get_audio_track_info(self):
        """
        Get original audio track information.
        """
        return self.export_data.get("audio_track", {})
    
    def get_video_track_info(self):
        """
        Get video track information.
        """
        return self.export_data.get("video_track", {})
    
    def get_enhancement_tracks(self):
        """
        Get list of enhancement tracks.
        """
        return self.export_data.get("enhancement_tracks", [])
    
    def get_noise_reduction_strength(self):
        """
        Get noise reduction strength from audio track.
        """
        audio_track = self.get_audio_track_info()
        processing = audio_track.get("processing", {})
        noise_reduction = processing.get("noise_reduction", {})
        return noise_reduction.get("strength", 0.5)
    
    def generate_project_file(self):
        """
        Generate a REAPER project file from loaded export data.
        Returns path to the generated .rpp file.
        """
        if not self.export_data:
            app_logger.error("No export data loaded")
            return None
        
        try:
            generator = ReaperProjectGenerator()
            project_path = generator.generate_project(self.export_data)
            return project_path
        except Exception as e:
            app_logger.error(f"Error generating project file: {e}")
            return None
