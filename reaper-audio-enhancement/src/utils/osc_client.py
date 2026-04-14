"""
OSC (Open Sound Control) client for communicating with REAPER.
Allows the app to trigger REAPER actions remotely via OSC messages.
"""

import socket
import struct
import time
from src.utils import app_logger


class OSCClient:
    """Send OSC messages to REAPER to trigger actions."""
    
    def __init__(self, host="127.0.0.1", port=9000):
        """
        Initialize OSC client.
        
        Args:
            host: REAPER host (default: localhost)
            port: REAPER OSC listen port (default: 9000)
        """
        self.host = host
        self.port = port
        self.socket = None
    
    def send_action(self, command_id, wait_ms=0):
        """
        Send OSC message to trigger a REAPER action.
        
        Args:
            command_id: REAPER command ID (e.g., "_ADD_VIDEO_TO_REAPER")
            wait_ms: Optional delay before sending (milliseconds)
        
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            if wait_ms > 0:
                time.sleep(wait_ms / 1000.0)
            
            # Create OSC message: /action/_COMMAND_ID
            message = f"/action/{command_id}"
            
            # Send via UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message.encode(), (self.host, self.port))
            sock.close()
            
            app_logger.info(f"OSC message sent: {message} to {self.host}:{self.port}")
            return True
        
        except Exception as e:
            app_logger.warning(f"Failed to send OSC message: {e}")
            return False
    
    def send_add_video_command(self, wait_ms=2000):
        """
        Send command to REAPER to add video to project.
        
        Args:
            wait_ms: Delay before sending (default: 2000ms for REAPER to load)
        
        Returns:
            bool: True if message sent successfully
        """
        return self.send_action("_ADD_VIDEO_TO_REAPER", wait_ms)
    
    def is_reaper_running(self):
        """
        Check if REAPER is running and OSC is enabled.
        
        Returns:
            bool: True if REAPER responds to OSC, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1.0)
            
            # Send a simple test message
            sock.sendto(b"/test", (self.host, self.port))
            
            sock.close()
            return True
        except Exception:
            return False


def get_osc_client(host="127.0.0.1", port=9000):
    """
    Get OSC client instance.
    
    Args:
        host: REAPER host
        port: REAPER OSC port
    
    Returns:
        OSCClient: OSC client instance
    """
    return OSCClient(host, port)
