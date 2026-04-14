"""
Video processor for stripping audio from video files.
Used during export to create clean video files without embedded audio.
"""

import subprocess
from pathlib import Path
from src.utils import app_logger


class VideoProcessor:
    """Process video files (strip audio, etc.)"""
    
    @staticmethod
    def strip_audio_from_video(input_video, output_video=None):
        """
        Strip audio from a video file using ffmpeg.
        
        Args:
            input_video: Path to input video file
            output_video: Path to output video file (without audio)
                         If None, creates output with _no_audio suffix
        
        Returns:
            Path to output video file if successful, None otherwise
        """
        try:
            input_path = Path(input_video)
            
            if not input_path.exists():
                app_logger.error(f"Input video not found: {input_video}")
                return None
            
            # Generate output path if not provided
            if output_video is None:
                output_path = input_path.parent / f"{input_path.stem}_no_audio{input_path.suffix}"
            else:
                output_path = Path(output_video)
            
            # Check if ffmpeg is available
            try:
                subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
            except (FileNotFoundError, subprocess.TimeoutExpired):
                app_logger.error("ffmpeg not found. Cannot strip audio from video.")
                return None
            
            # Use ffmpeg to copy video stream without audio
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-c:v', 'copy',  # Copy video codec (no re-encoding)
                '-an',  # No audio
                '-y',  # Overwrite output file
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                app_logger.info(f"Stripped audio from video: {input_path.name}")
                app_logger.info(f"Output: {output_path.name}")
                return output_path
            else:
                app_logger.error(f"Failed to strip audio from video: {input_path.name}")
                app_logger.error(f"ffmpeg error: {result.stderr}")
                return None
        
        except subprocess.TimeoutExpired:
            app_logger.error(f"Video processing timeout for: {input_video}")
            return None
        except Exception as e:
            app_logger.error(f"Error stripping audio from video: {e}")
            return None
