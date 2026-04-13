import cv2
import numpy as np
from src.utils import app_logger

class SceneDetector:
    def __init__(self):
        self.scene_types = [
            "storm",
            "car_ride",
            "outdoor",
            "indoor",
            "traffic",
            "quiet",
        ]
    
    def detect_scenes(self, video_path, interval=1.0):
        """
        Detect scene types from video at regular intervals.
        Returns list of (timestamp, scene_type, confidence) tuples.
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                app_logger.error(f"Failed to open video: {video_path}")
                return []
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * interval)
            
            detected_scenes = []
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps
                    scene_type, confidence = self._analyze_frame(frame)
                    
                    detected_scenes.append({
                        "timestamp": timestamp,
                        "scene_type": scene_type,
                        "confidence": confidence,
                    })
                
                frame_count += 1
            
            cap.release()
            
            app_logger.info(f"Detected {len(detected_scenes)} scenes from video")
            return detected_scenes
        except Exception as e:
            app_logger.error(f"Error detecting scenes: {e}")
            return []
    
    def _analyze_frame(self, frame):
        """
        Analyze a single frame to detect scene type.
        Uses basic heuristics based on color brightness and edges.
        """
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            h, w = frame.shape[:2]
            
            # Calculate brightness (V channel in HSV)
            brightness = np.mean(gray)
            
            # Calculate edge density (indicates complexity/detail)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            edge_density = np.mean(np.abs(laplacian))
            
            # Calculate saturation (color intensity)
            saturation = np.mean(hsv[:, :, 1])
            
            # Decision tree based on visual characteristics
            # Dark scenes with high edge density = storm
            if brightness < 100 and edge_density > 30:
                return "storm", 0.8
            
            # Bright scenes with moderate saturation = outdoor
            elif brightness > 120 and saturation > 50:
                return "outdoor", 0.75
            
            # Very dark scenes = indoor or car_ride
            elif brightness < 80:
                return "car_ride", 0.65
            
            # Medium brightness with high saturation = outdoor
            elif brightness > 100 and saturation > 80:
                return "outdoor", 0.7
            
            # High edge density = traffic or complex scene
            elif edge_density > 50:
                return "traffic", 0.6
            
            # Low saturation, medium brightness = indoor
            elif saturation < 40 and brightness > 80:
                return "indoor", 0.6
            
            # Default to outdoor (most common for sample)
            else:
                return "outdoor", 0.55
        except Exception as e:
            app_logger.error(f"Error analyzing frame: {e}")
            return "outdoor", 0.4
    
    def get_dominant_scene(self, detected_scenes):
        """
        Get the most common scene type from detected scenes.
        """
        try:
            if not detected_scenes:
                return None
            
            scene_counts = {}
            for scene in detected_scenes:
                scene_type = scene["scene_type"]
                scene_counts[scene_type] = scene_counts.get(scene_type, 0) + 1
            
            dominant = max(scene_counts, key=scene_counts.get)
            confidence = scene_counts[dominant] / len(detected_scenes)
            
            return {
                "scene_type": dominant,
                "confidence": confidence,
                "counts": scene_counts,
            }
        except Exception as e:
            app_logger.error(f"Error getting dominant scene: {e}")
            return None
