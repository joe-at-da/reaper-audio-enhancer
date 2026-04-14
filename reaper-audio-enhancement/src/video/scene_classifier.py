"""
Hybrid Scene Classification using ML.
Learns scene types from sample videos and classifies new videos without hardcoding.
"""

import numpy as np
import cv2
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from skimage import feature
import pickle
from src.utils import app_logger


class SceneClassifier:
    """
    ML-based scene classifier that learns from sample videos.
    Supports training on new scene types and classifying new videos.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize classifier.
        
        Args:
            model_path: Path to saved classifier model (optional)
        """
        self.classifier = None
        self.scaler = None
        self.scene_types = []
        self.model_path = model_path or Path.home() / ".reaper_audio_enhancement" / "scene_classifier.pkl"
        
        # Try to load existing model
        if self.model_path.exists():
            self.load_model()
    
    def extract_features(self, frame):
        """
        Extract ML features from a video frame.
        
        Args:
            frame: OpenCV frame (BGR)
        
        Returns:
            Feature vector (numpy array)
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Resize frame to consistent size for consistent HOG features
            frame_resized = cv2.resize(frame, (128, 128))
            gray_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
            
            # Feature 1: Color histogram (captures dominant colors)
            hist_b = cv2.calcHist([frame_resized], [0], None, [16], [0, 256])
            hist_g = cv2.calcHist([frame_resized], [1], None, [16], [0, 256])
            hist_r = cv2.calcHist([frame_resized], [2], None, [16], [0, 256])
            color_features = np.concatenate([hist_b.flatten(), hist_g.flatten(), hist_r.flatten()])
            
            # Feature 2: HOG (Histogram of Oriented Gradients) - consistent size
            hog_features = feature.hog(gray_resized, orientations=8, pixels_per_cell=(8, 8),
                                       cells_per_block=(2, 2), feature_vector=True)
            
            # Feature 3: Basic statistics
            brightness = np.mean(gray)
            contrast = np.std(gray)
            
            # Feature 4: Color channel means
            blue_mean = np.mean(frame[:, :, 0])
            green_mean = np.mean(frame[:, :, 1])
            red_mean = np.mean(frame[:, :, 2])
            
            # Feature 5: Edge density
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            edge_density = np.mean(np.abs(laplacian))
            
            # Combine all features into fixed-size vector
            all_features = np.concatenate([
                color_features,
                hog_features,
                np.array([brightness, contrast, blue_mean, green_mean, red_mean, edge_density])
            ])
            
            return all_features.astype(np.float32)
        except Exception as e:
            app_logger.error(f"Error extracting features: {e}")
            return None
    
    def train(self, training_videos):
        """
        Train classifier on sample videos.
        
        Args:
            training_videos: Dict of {scene_type: video_path}
                Example: {"rain": "sample_rain.mp4", "car": "sample_car.mp4"}
        
        Returns:
            bool: True if training successful
        """
        try:
            app_logger.info(f"Training scene classifier on {len(training_videos)} scene types...")
            
            training_features = []
            training_labels = []
            
            for scene_type, video_path in training_videos.items():
                app_logger.info(f"  Extracting features from {scene_type} video...")
                
                cap = cv2.VideoCapture(str(video_path))
                if not cap.isOpened():
                    app_logger.warning(f"Could not open video: {video_path}")
                    continue
                
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_interval = int(fps * 1.0)  # Sample every 1 second
                frame_count = 0
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if frame_count % frame_interval == 0:
                        features = self.extract_features(frame)
                        if features is not None:
                            training_features.append(features)
                            training_labels.append(scene_type)
                    
                    frame_count += 1
                
                cap.release()
                app_logger.info(f"    Extracted {len([l for l in training_labels if l == scene_type])} samples")
            
            if not training_features:
                app_logger.error("No training features extracted!")
                return False
            
            # Normalize features
            self.scaler = StandardScaler()
            training_features_normalized = self.scaler.fit_transform(training_features)
            
            # Train KNN classifier
            self.classifier = KNeighborsClassifier(n_neighbors=5)
            self.classifier.fit(training_features_normalized, training_labels)
            self.scene_types = list(training_videos.keys())
            
            # Save model
            self.save_model()
            
            app_logger.info(f"✓ Classifier trained on {len(self.scene_types)} scene types")
            return True
        except Exception as e:
            app_logger.error(f"Error training classifier: {e}")
            return False
    
    def classify_frame(self, frame):
        """
        Classify a single frame.
        
        Args:
            frame: OpenCV frame (BGR)
        
        Returns:
            Tuple of (scene_type, confidence)
        """
        if self.classifier is None:
            app_logger.warning("Classifier not trained. Using fallback detection.")
            return "outdoor", 0.5
        
        try:
            features = self.extract_features(frame)
            if features is None:
                return "outdoor", 0.5
            
            # Normalize features
            features_normalized = self.scaler.transform([features])
            
            # Predict
            scene_type = self.classifier.predict(features_normalized)[0]
            
            # Get confidence (distance to nearest neighbor)
            distances, indices = self.classifier.kneighbors(features_normalized, n_neighbors=1)
            confidence = 1.0 / (1.0 + distances[0][0])  # Convert distance to confidence
            confidence = min(0.95, max(0.5, confidence))
            
            return scene_type, confidence
        except Exception as e:
            app_logger.error(f"Error classifying frame: {e}")
            return "outdoor", 0.5
    
    def classify_video(self, video_path):
        """
        Classify all frames in a video and return dominant scene type.
        
        Args:
            video_path: Path to video file
        
        Returns:
            Dict with scene classification results
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                app_logger.error(f"Could not open video: {video_path}")
                return None
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * 1.0)  # Sample every 1 second
            frame_count = 0
            
            scene_predictions = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps
                    scene_type, confidence = self.classify_frame(frame)
                    scene_predictions.append({
                        "timestamp": timestamp,
                        "scene_type": scene_type,
                        "confidence": confidence
                    })
                
                frame_count += 1
            
            cap.release()
            
            # Find dominant scene type
            if not scene_predictions:
                return None
            
            scene_counts = {}
            for pred in scene_predictions:
                scene = pred["scene_type"]
                scene_counts[scene] = scene_counts.get(scene, 0) + 1
            
            dominant_scene = max(scene_counts.items(), key=lambda x: x[1])[0]
            avg_confidence = np.mean([p["confidence"] for p in scene_predictions])
            
            result = {
                "dominant_scene": dominant_scene,
                "confidence": avg_confidence,
                "predictions": scene_predictions,
                "scene_counts": scene_counts
            }
            
            app_logger.info(f"Video classified as: {dominant_scene} ({avg_confidence:.2f})")
            
            return result
        except Exception as e:
            app_logger.error(f"Error classifying video: {e}")
            return None
    
    def save_model(self):
        """Save trained model to disk."""
        try:
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            
            model_data = {
                "classifier": self.classifier,
                "scaler": self.scaler,
                "scene_types": self.scene_types
            }
            
            with open(self.model_path, "wb") as f:
                pickle.dump(model_data, f)
            
            app_logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            app_logger.error(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model from disk."""
        try:
            with open(self.model_path, "rb") as f:
                model_data = pickle.load(f)
            
            self.classifier = model_data["classifier"]
            self.scaler = model_data["scaler"]
            self.scene_types = model_data["scene_types"]
            
            app_logger.info(f"Model loaded from {self.model_path}")
            app_logger.info(f"Trained on scene types: {self.scene_types}")
        except Exception as e:
            app_logger.error(f"Error loading model: {e}")
    
    def is_trained(self):
        """Check if classifier is trained."""
        return self.classifier is not None


def get_scene_classifier(model_path=None):
    """
    Get or create scene classifier instance.
    
    Args:
        model_path: Optional path to saved model
    
    Returns:
        SceneClassifier instance
    """
    return SceneClassifier(model_path)
