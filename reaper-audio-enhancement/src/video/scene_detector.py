import cv2
import numpy as np
from src.utils import app_logger
from src.video.scene_classifier import get_scene_classifier

class SceneDetector:
    def __init__(self, use_ml_classifier=True):
        """
        Initialize scene detector.
        
        Args:
            use_ml_classifier: If True, use trained ML classifier if available
        """
        self.scene_types = [
            "storm",
            "car_ride",
            "outdoor",
            "indoor",
            "traffic",
            "quiet",
        ]
        
        # Try to load ML classifier if requested
        self.ml_classifier = None
        if use_ml_classifier:
            try:
                classifier = get_scene_classifier()
                if classifier.is_trained():
                    self.ml_classifier = classifier
                    app_logger.info(f"Using ML classifier trained on: {classifier.scene_types}")
            except Exception as e:
                app_logger.debug(f"ML classifier not available: {e}")
    
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
        Uses ML classifier if available, falls back to heuristic matching.
        """
        try:
            # Try ML classifier first if available
            if self.ml_classifier is not None:
                scene_type, confidence = self.ml_classifier.classify_frame(frame)
                return scene_type, confidence
            
            # Fallback to heuristic matching
            scene_type, confidence = self._match_scene_to_audio(None, frame)
            return scene_type, confidence
        except Exception as e:
            app_logger.error(f"Error analyzing frame: {e}")
            return "outdoor", 0.5
    
    def _match_scene_to_audio(self, features, frame):
        """
        Match frame features to available audio files.
        Uses visual cues to determine which audio would best match.
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Calculate visual characteristics
            brightness = np.mean(gray)
            saturation = np.mean(hsv[:, :, 1])
            
            # Detect water/rain patterns (blue/cyan colors with reflections)
            blue_channel = frame[:, :, 0]
            green_channel = frame[:, :, 1]
            red_channel = frame[:, :, 2]
            
            blue_intensity = np.mean(blue_channel)
            green_intensity = np.mean(green_channel)
            red_intensity = np.mean(red_channel)
            
            # Rain has blue > green > red (water droplets reflect blue light)
            # Sky has blue > red ≈ green (uniform blue)
            blue_dominance = blue_intensity - max(green_intensity, red_intensity)
            
            # Detect motion/traffic patterns (high edge density)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            edge_density = np.mean(np.abs(laplacian))
            
            # Score each available scene type
            scores = {}
            
            # Rain: Blue dominance (water), medium-high brightness, some edge detail
            # Rain can have lower edge density if blue dominance is strong
            rain_score = 0
            if blue_dominance > 15:
                rain_score = 0.8  # Strong blue dominance = likely rain
            elif blue_dominance > 5 and edge_density > 5:
                rain_score = 0.6  # Moderate blue + some detail
            scores["rain"] = rain_score
            
            # Car/Traffic: High edge density (road markings, vehicles), bright
            # Key: high edge density from road structure and vehicles
            scores["car_ride"] = (edge_density > 15) * 0.7 + (brightness > 100) * 0.2 + (saturation > 40) * 0.1
            
            # Storm: Dark, high edge density, blue dominance
            scores["storm"] = (brightness < 100) * 0.4 + (edge_density > 30) * 0.4 + (blue_dominance > 5) * 0.2
            
            # Outdoor/Nature: Bright, varied colors, natural saturation, moderate edges
            scores["outdoor"] = (brightness > 120) * 0.4 + (saturation > 50 and saturation < 150) * 0.4 + (edge_density > 10 and edge_density < 40) * 0.2
            
            # Indoor: Medium brightness, low saturation, some structure, low-medium edges
            # Must have low saturation to be indoor (car has higher saturation)
            scores["indoor"] = (brightness > 80 and brightness < 120) * 0.5 + (saturation < 40) * 0.4 + (edge_density > 10 and edge_density < 30) * 0.1
            
            # Find best match
            best_scene = max(scores.items(), key=lambda x: x[1])
            scene_type = best_scene[0]
            confidence = min(0.95, max(0.5, best_scene[1]))
            
            app_logger.debug(f"Frame analysis - brightness:{brightness:.0f}, saturation:{saturation:.0f}, blue:{blue_intensity:.0f}, edges:{edge_density:.1f}")
            app_logger.debug(f"Scene scores: {scores} → {scene_type} ({confidence:.2f})")
            
            return scene_type, confidence
        except Exception as e:
            app_logger.error(f"Error matching scene to audio: {e}")
            return "outdoor", 0.54
    
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
