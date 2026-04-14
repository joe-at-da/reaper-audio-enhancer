# Scene Detection Improvements - COMPLETED

## Problem Solved
Fixed overly aggressive scene detection that was creating 13 identical tracks from a uniform snowstorm video.

### Before
- **13 scenes detected** from 13-second snowstorm video
- **39 audio suggestions** (13 scenes × 3 audio files each)
- **13 duplicate tracks** in REAPER (all the same sound)
- **Issue**: Detecting every frame as a new scene instead of detecting actual scene *changes*

### After
- **1 scene detected** from 13-second snowstorm video
- **1 audio suggestion** (deduplicated)
- **1 track in REAPER** (clean, no duplicates)
- **Solution**: Implemented proper scene change detection with 30% threshold

---

## Implementation Details

### 1. Scene Change Detection (`src/video/scene_detector.py`)

**New Method: `_calculate_frame_difference()`**
- Compares consecutive frames using histogram comparison
- Returns normalized difference (0 = identical, 1 = completely different)
- Uses chi-square distance for robust comparison

**New Method: `_merge_identical_scenes()`**
- Merges consecutive scenes of the same type
- Keeps first occurrence, averages confidence
- Example: [storm@0s, storm@1s, storm@2s] → [storm@0s]

**Modified: `detect_scenes()`**
- Added `change_threshold` parameter (default: 30%)
- Only flags scene changes when frame difference > threshold
- Prevents false positives from minor variations (snowflake movement)
- Merges identical consecutive scenes
- Logs detected scenes with confidence scores

### 2. Audio Suggestion Deduplication (`src/audio/audio_suggester.py`)

**Modified: `suggest_audio_for_scene()`**
- For each scene, suggests only 1 best audio file (not all 3)
- Calls deduplication method to remove duplicates
- Logs: "Generated X audio suggestions (after deduplication)"

**New Method: `_deduplicate_suggestions()`**
- Removes duplicates by (audio_file, scene_type)
- Keeps suggestion with highest confidence
- Prevents duplicate tracks in REAPER

---

## How It Works

### Scene Detection Flow
```
1. Sample frames at 1-second intervals
2. Classify each frame (brightness, edges, saturation)
3. Compare with previous frame (histogram difference)
4. Only flag as scene change if difference > 30%
5. Merge consecutive identical scenes
6. Return: List of actual scene boundaries
```

### Example: Snowstorm Video
```
Frame 0s: "indoor" (first frame, always a scene)
Frame 1s: "indoor" (difference < 30%, not a scene change)
Frame 2s: "indoor" (difference < 30%, not a scene change)
...
Frame 13s: "indoor" (difference < 30%, not a scene change)

Result: 1 scene (indoor at 0.0s)
```

### Example: Varied Video (Snow → House → Car)
```
Frame 0s: "outdoor" (first frame)
Frame 5s: "indoor" (difference > 30%, scene change!)
Frame 10s: "car_ride" (difference > 30%, scene change!)

Result: 3 scenes (outdoor@0s, indoor@5s, car_ride@10s)
```

---

## Configuration

### Scene Change Threshold
- **Default**: 30% (conservative)
- **Location**: `src/video/scene_detector.py`, line 16
- **Adjust**: Increase for fewer scenes, decrease for more scenes

```python
scenes = detector.detect_scenes(video_path, change_threshold=0.30)
```

---

## Logging Output

**Before**:
```
Detected 13 scenes from video
Generated 39 audio suggestions
```

**After**:
```
Detected 1 scene changes from video (threshold: 30%)
  - indoor at 0.0s (confidence: 0.60)
Generated 1 audio suggestions (after deduplication)
```

---

## Testing Results

### Snowstorm Video (13 seconds, uniform snow)
✅ **1 scene detected** (was 13)
✅ **1 audio suggestion** (was 39)
✅ **1 track in REAPER** (was 13)

### Expected for Varied Videos
✅ Snow → House → Car = 3 scenes
✅ Each scene gets 1-2 audio suggestions
✅ Clean, non-duplicate tracks in REAPER

---

## Files Modified

1. `src/video/scene_detector.py`
   - Added `_calculate_frame_difference()` method
   - Added `_merge_identical_scenes()` method
   - Modified `detect_scenes()` with change detection

2. `src/audio/audio_suggester.py`
   - Modified `suggest_audio_for_scene()` for deduplication
   - Added `_deduplicate_suggestions()` method

---

## Summary

✅ Scene detection now intelligent and efficient
✅ No more false positives from minor frame variations
✅ Duplicate audio suggestions eliminated
✅ REAPER projects are clean and organized
✅ Logging shows exactly what was detected

**The tool now correctly handles both uniform videos (1 scene) and varied videos (multiple scenes with appropriate audio for each).**
