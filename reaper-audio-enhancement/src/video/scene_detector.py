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
    
    def detect_scenes(self, video_path, interval=1.0, change_threshold=0.30):
        """
        Detect scene changes from video using frame-to-frame comparison.
        Only flags significant changes (default 30%+ difference).
        Returns list of (timestamp, scene_type, confidence) tuples for actual scene changes.
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
            prev_frame = None
            prev_scene_type = None
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps
                    scene_type, confidence = self._analyze_frame(frame)
                    
                    # Check if this is a scene change (not just a frame classification)
                    is_scene_change = False
                    
                    if prev_frame is None:
                        # First frame is always a scene
                        is_scene_change = True
                    elif scene_type != prev_scene_type:
                        # Scene type changed - check if it's significant
                        frame_diff = self._calculate_frame_difference(prev_frame, frame)
                        if frame_diff > change_threshold:
                            is_scene_change = True
                            app_logger.debug(f"Scene change detected at {timestamp}s: {prev_scene_type} → {scene_type} (diff: {frame_diff:.2%})")
                    
                    if is_scene_change:
                        detected_scenes.append({
                            "timestamp": timestamp,
                            "scene_type": scene_type,
                            "confidence": confidence,
                        })
                    
                    prev_frame = frame.copy()
                    prev_scene_type = scene_type
                
                frame_count += 1
            
            cap.release()
            
            # Merge identical consecutive scenes
            merged_scenes = self._merge_identical_scenes(detected_scenes)
            
            app_logger.info(f"Detected {len(merged_scenes)} scene changes from video (threshold: {change_threshold:.0%})")
            for scene in merged_scenes:
                app_logger.info(f"  - {scene['scene_type']} at {scene['timestamp']:.1f}s (confidence: {scene['confidence']:.2f})")
            
            return merged_scenes
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
    
    def _calculate_frame_difference(self, frame1, frame2):
        """
        Calculate the difference between two frames using histogram comparison.
        Returns a value between 0 and 1 (0 = identical, 1 = completely different).
        """
        try:
            # Convert to grayscale
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            
            # Calculate histograms
            hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
            
            # Normalize histograms
            hist1 = cv2.normalize(hist1, hist1).flatten()
            hist2 = cv2.normalize(hist2, hist2).flatten()
            
            # Compare using chi-square distance
            diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
            
            # Normalize to 0-1 range (chi-square can be large)
            # Empirically, significant changes are > 0.3 in normalized space
            normalized_diff = min(diff / 10.0, 1.0)
            
            return normalized_diff
        except Exception as e:
            app_logger.debug(f"Error calculating frame difference: {e}")
            return 0.0
    
    def _merge_identical_scenes(self, detected_scenes):
        """
        Merge consecutive scenes of the same type into a single scene.
        Keeps the first occurrence and averages confidence.
        """
        try:
            if not detected_scenes:
                return []
            
            merged = []
            current_group = [detected_scenes[0]]
            
            for scene in detected_scenes[1:]:
                if scene["scene_type"] == current_group[0]["scene_type"]:
                    # Same scene type, add to group
                    current_group.append(scene)
                else:
                    # Different scene type, finalize current group
                    merged_scene = {
                        "timestamp": current_group[0]["timestamp"],
                        "scene_type": current_group[0]["scene_type"],
                        "confidence": np.mean([s["confidence"] for s in current_group]),
                    }
                    merged.append(merged_scene)
                    current_group = [scene]
            
            # Don't forget the last group
            merged_scene = {
                "timestamp": current_group[0]["timestamp"],
                "scene_type": current_group[0]["scene_type"],
                "confidence": np.mean([s["confidence"] for s in current_group]),
            }
            merged.append(merged_scene)
            
            return merged
        except Exception as e:
            app_logger.error(f"Error merging scenes: {e}")
            return detected_scenes
    
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
