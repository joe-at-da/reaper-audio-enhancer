from pathlib import Path
from datetime import datetime
from src.utils import app_logger


class ReaperProjectGenerator:
    """
    Generate REAPER project files (.rpp) with audio and video tracks.
    Uses REAPER's native text format instead of XML.
    """
    
    def __init__(self):
        self.export_dir = Path.home() / ".reaper_audio_enhancement" / "exports"
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_project(self, export_data):
        """
        Generate a REAPER project file from export data.
        Returns path to the generated .rpp file.
        """
        try:
            # Create project content in REAPER format
            project_content = self._create_project_content(export_data)
            
            # Save project file
            project_path = self._save_project(project_content)
            app_logger.info(f"REAPER project generated: {project_path}")
            return project_path
        except Exception as e:
            app_logger.error(f"Error generating REAPER project: {e}")
            return None
    
    def _create_project_content(self, export_data):
        """Create REAPER project content in native format."""
        lines = []
        
        # REAPER project header (minimal, valid format)
        lines.append("<REAPER_PROJECT 0.1 \"6.82\" 1629820800")
        lines.append("  SAMPLERATE 44100 5 2")
        lines.append("  TEMPO 120 4 4")
        lines.append("  PLAYRATE 1 0 0.25 8")
        lines.append("  CURSOR 0")
        lines.append("  SELECTION 0 0")
        lines.append("  ZOOM 6.41 0 0")
        lines.append("  VZOOM 0 0")
        lines.append("  MASTER_VOLUME 1.0 0 -1 -1 1")
        lines.append("  MASTER_FX 0")
        lines.append("  MASTER_SEL 0")
        lines.append("")
        
        # Add tracks
        track_index = 0
        
        # Add original audio track
        audio_track = export_data.get("audio_track", {})
        if audio_track.get("file"):
            lines.extend(self._create_audio_track(
                track_index,
                audio_track.get("name", "Original Audio"),
                audio_track.get("file"),
                0,
                1.0,
                0,
                0
            ))
            track_index += 1
        
        # Add video track
        video_track = export_data.get("video_track", {})
        if video_track.get("file"):
            lines.extend(self._create_video_track(
                track_index,
                video_track.get("name", "Video"),
                video_track.get("file")
            ))
            track_index += 1
        
        # Add enhancement tracks
        for track_info in export_data.get("enhancement_tracks", []):
            lines.extend(self._create_audio_track(
                track_index,
                track_info.get("name", f"Enhancement {track_index}"),
                track_info.get("file"),
                track_info.get("start_time", 0),
                track_info.get("volume", 1.0),
                track_info.get("fade_in", 0),
                track_info.get("fade_out", 0)
            ))
            track_index += 1
        
        lines.append(">")
        return "\n".join(lines)
    
    def _create_audio_track(self, track_index, name, file_path, start_time, volume, fade_in, fade_out):
        """Create audio track lines."""
        lines = []
        lines.append(f"  <TRACK {track_index}")
        lines.append(f"    NAME {name}")
        lines.append(f"    VOLPAN {volume} 0 -1 -1 1")
        lines.append(f"    MUTESOLO 0 0 0")
        lines.append(f"    IPHASE 0")
        lines.append(f"    PLAYOFFS 0 1")
        lines.append(f"    CSURF 0 0 0")
        lines.append(f"    TRACKHEIGHT 0 0 0")
        lines.append(f"    INQ 0 0 0 0.5 100 0 0 100")
        lines.append(f"    NCHAN 2")
        lines.append(f"    FX 0")
        lines.append(f"    AUXFLAGS 0")
        lines.append(f"    BUSCOMP 0 0 0 0 0 -1 -1 -1")
        lines.append(f"    BUSCOMP 0 0 0 0 0 -1 -1 -1")
        lines.append(f"    COMPMODE 0")
        lines.append(f"    Pan2 0")
        
        # Add media item
        if file_path:
            lines.append(f"    <ITEM")
            lines.append(f"      POSITION {start_time}")
            lines.append(f"      SNAPOFFS 0")
            lines.append(f"      LENGTH 10")
            lines.append(f"      BASE_PITCH 1")
            lines.append(f"      PLAYRATE 1")
            lines.append(f"      CHANMODE 0")
            lines.append(f"      GUID {self._generate_guid()}")
            lines.append(f"      <SOURCE WAVE")
            lines.append(f"        FILE \"{file_path}\"")
            lines.append(f"      >")
            lines.append(f"      <FADES")
            lines.append(f"        FADEIN 1 {fade_in} 0 1 0 0")
            lines.append(f"        FADEOUT 1 {fade_out} 0 1 0 0")
            lines.append(f"      >")
            lines.append(f"    >")
        
        lines.append(f"  >")
        return lines
    
    def _create_video_track(self, track_index, name, file_path):
        """Create video track lines."""
        lines = []
        lines.append(f"  <TRACK {track_index}")
        lines.append(f"    NAME {name}")
        lines.append(f"    VOLPAN 1 0 -1 -1 1")
        lines.append(f"    MUTESOLO 0 0 0")
        lines.append(f"    IPHASE 0")
        lines.append(f"    PLAYOFFS 0 1")
        lines.append(f"    CSURF 0 0 0")
        lines.append(f"    TRACKHEIGHT 0 0 0")
        lines.append(f"    INQ 0 0 0 0.5 100 0 0 100")
        lines.append(f"    NCHAN 2")
        lines.append(f"    FX 0")
        lines.append(f"    AUXFLAGS 0")
        
        # Add media item with VIDEO source
        if file_path:
            # Get video duration
            duration = self._get_video_duration(file_path)
            
            lines.append(f"    <ITEM")
            lines.append(f"      POSITION 0")
            lines.append(f"      SNAPOFFS 0")
            lines.append(f"      LENGTH {duration}")
            lines.append(f"      BASE_PITCH 1")
            lines.append(f"      PLAYRATE 1")
            lines.append(f"      CHANMODE 0")
            lines.append(f"      GUID {self._generate_guid()}")
            lines.append(f"      <SOURCE VIDEOFILE")
            lines.append(f"        FILE \"{file_path}\"")
            lines.append(f"      >")
            lines.append(f"    >")
        
        lines.append(f"  >")
        return lines
    
    def _get_video_duration(self, file_path):
        """Get video duration in seconds."""
        try:
            import subprocess
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
                 '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1', 
                 str(file_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
        except Exception as e:
            app_logger.debug(f"Could not get video duration: {e}")
        
        # Default to 20 seconds if we can't get duration
        return 20.0
    
    def _generate_guid(self):
        """Generate a simple GUID for track items."""
        import uuid
        return str(uuid.uuid4()).replace('-', '')[:32]
    
    def _save_project(self, content):
        """Save project to .rpp file."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"project_{timestamp}.rpp"
            project_path = self.export_dir / filename
            
            with open(project_path, 'w') as f:
                f.write(content)
            
            return project_path
        except Exception as e:
            app_logger.error(f"Error saving project file: {e}")
            return None
