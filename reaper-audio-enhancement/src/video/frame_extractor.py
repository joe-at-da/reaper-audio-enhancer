import cv2
import numpy as np
from pathlib import Path
from src.utils import app_logger

class FrameExtractor:
    def __init__(self):
        self.frames = []
        self.fps = 0
        self.total_frames = 0
        self.duration = 0
    
    def load_video(self, video_path):
        """
        Load video file and extract metadata.
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                app_logger.error(f"Failed to open video: {video_path}")
                return False
            
            self.fps = cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            app_logger.info(f"Video loaded: {self.total_frames} frames, {self.fps} fps, {self.duration:.2f}s")
            cap.release()
            return True
        except Exception as e:
            app_logger.error(f"Error loading video: {e}")
            return False
    
    def extract_keyframes(self, video_path, interval=1.0):
        """
        Extract keyframes at regular intervals.
        interval: seconds between keyframes
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                app_logger.error(f"Failed to open video: {video_path}")
                return []
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * interval)
            
            keyframes = []
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    keyframes.append({
                        "frame_number": frame_count,
                        "timestamp": frame_count / fps,
                        "data": frame,
                    })
                
                frame_count += 1
            
            cap.release()
            
            app_logger.info(f"Extracted {len(keyframes)} keyframes from video")
            return keyframes
        except Exception as e:
            app_logger.error(f"Error extracting keyframes: {e}")
            return []
    
    def get_frame_at_time(self, video_path, timestamp):
        """
        Get a single frame at specific timestamp.
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                app_logger.error(f"Failed to open video: {video_path}")
                return None
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(timestamp * fps)
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                return frame
            return None
        except Exception as e:
            app_logger.error(f"Error getting frame at time: {e}")
            return None
    
    def resize_frame(self, frame, width=320):
        """
        Resize frame for processing.
        """
        try:
            h, w = frame.shape[:2]
            ratio = width / w
            new_h = int(h * ratio)
            return cv2.resize(frame, (width, new_h))
        except Exception as e:
            app_logger.error(f"Error resizing frame: {e}")
            return frame
