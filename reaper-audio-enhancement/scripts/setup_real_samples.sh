#!/bin/bash
# Setup real sample video and audio from downloaded video file
# Usage: bash setup_real_samples.sh /path/to/video.mp4

set -e

if [ $# -eq 0 ]; then
    echo "Usage: bash setup_real_samples.sh /path/to/video.mp4"
    echo ""
    echo "Example:"
    echo "  bash setup_real_samples.sh /Users/joebradley/Downloads/snow-video-with-shit-audio.mp4"
    exit 1
fi

VIDEO_INPUT="$1"
SAMPLE_DIR="$(dirname "$0")/../assets/sample_files"
SAMPLE_VIDEO="$SAMPLE_DIR/sample_video.mp4"
SAMPLE_AUDIO="$SAMPLE_DIR/sample_audio.wav"

# Check if input file exists
if [ ! -f "$VIDEO_INPUT" ]; then
    echo "✗ Error: File not found: $VIDEO_INPUT"
    exit 1
fi

echo "Setting up real samples..."
echo "  Input video: $VIDEO_INPUT"
echo "  Sample video: $SAMPLE_VIDEO"
echo "  Sample audio: $SAMPLE_AUDIO"
echo ""

# Create sample directory
mkdir -p "$SAMPLE_DIR"

# Copy video file
echo "1. Copying video file..."
cp "$VIDEO_INPUT" "$SAMPLE_VIDEO"
echo "   ✓ Video: $(ls -lh "$SAMPLE_VIDEO" | awk '{print $5}')"

# Extract audio from video
echo "2. Extracting audio from video..."
ffmpeg -i "$VIDEO_INPUT" -q:a 9 -n "$SAMPLE_AUDIO" 2>&1 | grep -E "Duration|Stream|Output" || true
echo "   ✓ Audio: $(ls -lh "$SAMPLE_AUDIO" | awk '{print $5}')"

# Verify files
echo ""
echo "3. Verifying files..."
echo "   Video:"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1:nokey=1 "$SAMPLE_VIDEO" 2>/dev/null | head -1 | xargs -I {} echo "     Duration: {} seconds"
echo "   Audio:"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1:nokey=1 "$SAMPLE_AUDIO" 2>/dev/null | head -1 | xargs -I {} echo "     Duration: {} seconds"

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Run the app: bash launch.sh demo"
echo "  2. Complete the workflow"
echo "  3. Open REAPER"
echo "  4. View > Video Window (Cmd+Shift+V)"
echo "  5. Click Play"
echo "  6. You'll see the real snowstorm video with the extracted audio!"
