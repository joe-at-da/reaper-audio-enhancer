# Scene Detection Approaches - Analysis

How to detect scenes without hardcoding thresholds for each type.

## Current Approach (Hardcoded)

**What we have now**:
- Hardcoded thresholds for rain, car, storm, outdoor, indoor
- Works for 3 specific videos
- Fails for new scene types (fire, underwater, etc.)

**Problem**: Not generalizable. Adding a fire video would require rewriting the thresholds.

---

## Option 1: Pre-trained Deep Learning Models (BEST)

**What it is**: Use a pre-trained neural network that already knows 1000+ scene types

**How it works**:
1. Load pre-trained ResNet50 from ImageNet
2. Pass frame through network
3. Get probability distribution over 1000 classes
4. Pick top class (e.g., "rain", "highway", "fire", etc.)

**Advantages**:
- ✅ Works for ANY scene type (1000+ classes)
- ✅ No hardcoding needed
- ✅ Highly accurate
- ✅ Transfer learning (trained on millions of images)

**Disadvantages**:
- ❌ Requires PyTorch or TensorFlow (not installed)
- ❌ Slower (neural network inference)
- ❌ Adds ~500MB dependency

**Implementation**:
```python
from torchvision import models, transforms
import torch

# Load pre-trained ResNet50
model = models.resnet50(pretrained=True)
model.eval()

# Classify frame
frame_tensor = transforms.ToTensor()(frame)
with torch.no_grad():
    output = model(frame_tensor.unsqueeze(0))
    class_idx = output.argmax(1).item()
    class_name = imagenet_classes[class_idx]  # e.g., "rain", "highway"
```

**Effort**: 2-3 hours (install PyTorch, integrate, test)

---

## Option 2: Unsupervised Clustering (MEDIUM)

**What it is**: Let the algorithm discover scene types automatically

**How it works**:
1. Extract features from all frames (color histogram, HOG, etc.)
2. Use KMeans clustering to group similar frames
3. Map clusters to available audio files
4. New videos automatically get clustered

**Advantages**:
- ✅ No hardcoding needed
- ✅ Works with any number of scene types
- ✅ Uses libraries we already have (sklearn)
- ✅ Fast

**Disadvantages**:
- ❌ Requires training on sample videos first
- ❌ Clusters may not match human intuition
- ❌ Need to label clusters manually

**Implementation**:
```python
from sklearn.cluster import KMeans

# Extract features from all frames
features = []
for frame in video_frames:
    features.append(extract_features(frame))

# Cluster into N groups
kmeans = KMeans(n_clusters=3)  # 3 clusters for rain/car/snow
labels = kmeans.fit_predict(features)

# Map clusters to audio
cluster_to_audio = {0: "rain.wav", 1: "car_engine.wav", 2: "ambient_nature.wav"}
```

**Effort**: 4-6 hours (feature engineering, clustering, validation)

---

## Option 3: Hybrid Approach (RECOMMENDED)

**What it is**: Combine unsupervised clustering with optional pre-trained models

**How it works**:
1. **Phase 1 (Setup)**: User provides sample videos with labels
   - App extracts features from each video
   - Learns what "rain" looks like, what "car" looks like, etc.
   - Stores feature profiles for each scene type

2. **Phase 2 (Detection)**: For new videos
   - Extract features from new video
   - Compare to learned profiles
   - Find closest match
   - Suggest matching audio

**Advantages**:
- ✅ No hardcoding
- ✅ Learns from user's videos
- ✅ Works with any scene type
- ✅ Uses libraries we have
- ✅ Fast and lightweight

**Disadvantages**:
- ❌ Requires initial training phase
- ❌ Accuracy depends on sample quality

**Implementation**:
```python
from sklearn.neighbors import KNeighborsClassifier

# Training phase (one-time)
training_features = []
training_labels = []
for scene_type in ["rain", "car", "snow"]:
    for frame in get_frames(f"sample_{scene_type}.mp4"):
        features = extract_features(frame)
        training_features.append(features)
        training_labels.append(scene_type)

# Train classifier
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(training_features, training_labels)

# Detection phase (for new videos)
for frame in new_video:
    features = extract_features(frame)
    scene_type = classifier.predict([features])[0]
    audio = audio_map[scene_type]
```

**Effort**: 3-4 hours (implement training, detection, validation)

---

## Option 4: Semantic Segmentation (ADVANCED)

**What it is**: Identify WHAT'S IN the scene (rain, cars, sky, etc.) not just classify it

**How it works**:
1. Use semantic segmentation model (e.g., DeepLabV3)
2. Identify objects in frame (rain pixels, car pixels, sky pixels)
3. Determine scene type based on object composition

**Advantages**:
- ✅ Most accurate
- ✅ Understands scene composition
- ✅ Can detect multiple scene types in one frame

**Disadvantages**:
- ❌ Requires heavy model (TensorFlow/PyTorch)
- ❌ Slow
- ❌ Overkill for our use case

**Effort**: 6-8 hours

---

## Recommendation

**For your use case, I recommend Option 3 (Hybrid Approach)**:

1. **Why**: 
   - No hardcoding
   - Works with any scene type
   - Uses libraries we already have
   - Reasonable effort (3-4 hours)
   - User can add new scene types by providing sample videos

2. **How it would work**:
   - User provides sample videos: `sample_rain.mp4`, `sample_car.mp4`, `sample_fire.mp4`, etc.
   - App learns feature profiles for each
   - New videos automatically classified
   - No threshold adjustments needed

3. **Example workflow**:
   ```
   User: "I want to add fire scene detection"
   User: Provides sample_fire.mp4
   App: Extracts features, trains classifier
   User: Uploads new fire video
   App: Automatically detects as "fire", suggests fire audio
   ```

---

## Comparison Table

| Approach | Hardcoding | Generalization | Speed | Effort | Dependencies |
|----------|-----------|-----------------|-------|--------|--------------|
| Current (Hardcoded) | ✅ Yes | ❌ No | ⚡ Fast | 0h | None |
| Pre-trained DL | ❌ No | ✅ Excellent | 🐢 Slow | 2-3h | PyTorch/TF |
| Unsupervised | ❌ No | ✅ Good | ⚡ Fast | 4-6h | sklearn |
| **Hybrid (Recommended)** | ❌ No | ✅ Excellent | ⚡ Fast | 3-4h | sklearn |
| Semantic Seg | ❌ No | ✅ Perfect | 🐢 Slow | 6-8h | PyTorch/TF |

---

## Next Steps

1. **Short term**: Keep current hardcoded approach for now (works for 3 videos)
2. **Medium term**: Implement Hybrid approach (3-4 hours)
3. **Long term**: Consider pre-trained models if accuracy becomes critical

Would you like me to implement the Hybrid approach?
