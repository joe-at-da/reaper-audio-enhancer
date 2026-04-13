from pythonosc import udp_client
from src.utils import app_logger, config

class ReaperOSCClient:
    def __init__(self, host=None, port=None):
        self.host = host or config.get("osc_host", "127.0.0.1")
        self.port = port or config.get("osc_port", 9000)
        self.client = None
        self.connected = False
    
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
        Create a new track in REAPER.
        track_type: "audio" or "video"
        """
        try:
            self.send_command("/action", 40001)
            
            return True
        except Exception as e:
            app_logger.error(f"Error creating track: {e}")
            return False
    
    def insert_media(self, track_index, file_path, position=0):
        """
        Insert media file on track.
        """
        try:
            self.send_command("/action", 40001)
            
            return True
        except Exception as e:
            app_logger.error(f"Error inserting media: {e}")
            return False
    
    def set_track_name(self, track_index, name):
        """
        Set track name.
        """
        try:
            self.send_command(f"/track/{track_index}/name", name)
            return True
        except Exception as e:
            app_logger.error(f"Error setting track name: {e}")
            return False
