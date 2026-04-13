from pythonosc import udp_client
from src.utils import app_logger, config
import time


class OSCImporter:
    """
    Import audio enhancement results into REAPER via OSC.
    """
    
    def __init__(self, host=None, port=None):
        self.host = host or config.get("osc_host", "127.0.0.1")
        self.port = port or config.get("osc_port", 9000)
        self.client = None
        self.connected = False
        self.track_count = 0
    
    def connect(self):
        """
        Connect to REAPER via OSC.
        """
        try:
            self.client = udp_client.SimpleUDPClient(self.host, self.port)
            self.connected = True
            app_logger.info(f"Connected to REAPER at {self.host}:{self.port}")
            return True
        except Exception as e:
            app_logger.error(f"Failed to connect to REAPER: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """
        Disconnect from REAPER.
        """
        self.connected = False
        self.client = None
    
    def send_command(self, address, *args):
        """
        Send OSC command to REAPER.
        """
        try:
            if not self.connected:
                if not self.connect():
                    return False
            
            self.client.send_message(address, args)
            app_logger.debug(f"Sent OSC: {address} {args}")
            return True
        except Exception as e:
            app_logger.error(f"Error sending OSC command: {e}")
            return False
    
    def create_track(self, track_name, track_type="audio"):
        """
        Create a new track in REAPER via OSC.
        track_type: "audio" or "video"
        Returns track index if successful, -1 otherwise.
        """
        try:
            self.send_command("/action", 40001)
            time.sleep(0.1)
            
            track_index = self.track_count
            self.track_count += 1
            
            self.set_track_name(track_index, track_name)
            
            app_logger.info(f"Created track {track_index}: {track_name}")
            return track_index
        except Exception as e:
            app_logger.error(f"Error creating track: {e}")
            return -1
    
    def set_track_name(self, track_index, name):
        """
        Set track name via OSC.
        """
        try:
            self.send_command(f"/track/{track_index}/name", name)
            return True
        except Exception as e:
            app_logger.error(f"Error setting track name: {e}")
            return False
    
    def insert_media_item(self, track_index, file_path, position=0, length=None):
        """
        Insert media file on track at position.
        position: start time in seconds
        length: duration in seconds (None = auto-detect)
        """
        try:
            self.send_command(f"/track/{track_index}/media/insert", file_path, position, length or 0)
            app_logger.info(f"Inserted media on track {track_index}: {file_path} at {position}s")
            return True
        except Exception as e:
            app_logger.error(f"Error inserting media: {e}")
            return False
    
    def set_track_volume(self, track_index, volume):
        """
        Set track volume (0.0 to 1.0).
        """
        try:
            self.send_command(f"/track/{track_index}/volume", volume)
            return True
        except Exception as e:
            app_logger.error(f"Error setting track volume: {e}")
            return False
    
    def set_item_fade(self, track_index, item_index, fade_in=0, fade_out=0):
        """
        Set fade in/out for media item.
        fade_in, fade_out: duration in seconds
        """
        try:
            self.send_command(f"/track/{track_index}/item/{item_index}/fade_in", fade_in)
            self.send_command(f"/track/{track_index}/item/{item_index}/fade_out", fade_out)
            return True
        except Exception as e:
            app_logger.error(f"Error setting item fade: {e}")
            return False
    
    def apply_noise_reduction(self, track_index, strength):
        """
        Apply noise reduction effect to track.
        strength: 0.0 to 1.0
        """
        try:
            self.send_command(f"/track/{track_index}/fx/noise_reduction", strength)
            return True
        except Exception as e:
            app_logger.error(f"Error applying noise reduction: {e}")
            return False
    
    def import_from_data(self, export_data):
        """
        Import complete project from export data.
        """
        try:
            if not self.connected:
                if not self.connect():
                    return False
            
            self.track_count = 0
            
            audio_track = export_data.get("audio_track", {})
            if audio_track.get("file"):
                self.create_track(audio_track.get("name", "Original Audio"), "audio")
                self.insert_media_item(0, audio_track.get("file"), 0)
                
                noise_reduction = audio_track.get("processing", {}).get("noise_reduction", {})
                if noise_reduction.get("enabled"):
                    strength = noise_reduction.get("strength", 0.5)
                    self.apply_noise_reduction(0, strength)
            
            video_track = export_data.get("video_track", {})
            if video_track.get("file"):
                self.create_track(video_track.get("name", "Video"), "video")
                self.insert_media_item(1, video_track.get("file"), 0)
            
            for track_info in export_data.get("enhancement_tracks", []):
                track_idx = self.create_track(track_info.get("name", "Enhancement"), "audio")
                if track_idx >= 0:
                    self.insert_media_item(
                        track_idx,
                        track_info.get("file"),
                        track_info.get("start_time", 0),
                        track_info.get("duration")
                    )
                    
                    volume = track_info.get("volume", 1.0)
                    self.set_track_volume(track_idx, volume)
                    
                    fade_in = track_info.get("fade_in", 0)
                    fade_out = track_info.get("fade_out", 0)
                    if fade_in > 0 or fade_out > 0:
                        self.set_item_fade(track_idx, 0, fade_in, fade_out)
            
            app_logger.info("Successfully imported all tracks via OSC")
            return True
        except Exception as e:
            app_logger.error(f"Error importing from data: {e}")
            return False
