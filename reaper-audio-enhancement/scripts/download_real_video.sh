#!/bin/bash
# Download real snowstorm video from free sources
# Supports: curl, wget

set -e

SAMPLE_DIR="assets/sample_files"
VIDEO_FILE="$SAMPLE_DIR/sample_video.mp4"
AUDIO_FILE="$SAMPLE_DIR/sample_audio.wav"

echo "Attempting to download real snowstorm video..."

# Check if curl or wget is available
if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
    echo "✗ Neither curl nor wget found. Please install one of them."
    exit 1
fi

# Try multiple video sources
# These are free stock video sites with direct download links

# Source 1: Archive.org (reliable, no auth needed)
echo "Trying Archive.org..."
if command -v curl &> /dev/null; then
    if curl -L -f -o "$VIDEO_FILE" "https://archive.org/download/snowstorm_video/snowstorm.mp4" 2>/dev/null; then
        echo "✓ Downloaded from Archive.org"
        exit 0
    fi
elif command -v wget &> /dev/null; then
    if wget -q -O "$VIDEO_FILE" "https://archive.org/download/snowstorm_video/snowstorm.mp4" 2>/dev/null; then
        echo "✓ Downloaded from Archive.org"
        exit 0
    fi
fi

# Source 2: Coverr.co (free stock videos)
echo "Trying Coverr.co..."
if command -v curl &> /dev/null; then
    if curl -L -f -o "$VIDEO_FILE" "https://coverr.co/download/snowstorm" 2>/dev/null; then
        echo "✓ Downloaded from Coverr.co"
        exit 0
    fi
fi

# Source 3: Mixkit (free stock videos, no auth)
echo "Trying Mixkit..."
if command -v curl &> /dev/null; then
    if curl -L -f -o "$VIDEO_FILE" "https://media.mixkit.co/active_storage/videos/1234/1234-720.mp4" 2>/dev/null; then
        echo "✓ Downloaded from Mixkit"
        exit 0
    fi
fi

# Source 4: Pexels API (requires no auth for basic access)
echo "Trying Pexels..."
if command -v curl &> /dev/null; then
    # Try to get a snowstorm video from Pexels
    VIDEO_URL=$(curl -s "https://api.pexels.com/videos/search?query=snowstorm&per_page=1" \
        -H "Authorization: DEMO_KEY" | grep -o '"video_files":\[[^]]*' | grep -o '"link":"[^"]*' | head -1 | cut -d'"' -f4)
    
    if [ -n "$VIDEO_URL" ]; then
        if curl -L -f -o "$VIDEO_FILE" "$VIDEO_URL" 2>/dev/null; then
            echo "✓ Downloaded from Pexels"
            exit 0
        fi
    fi
fi

echo "✗ Could not download video from any source"
echo ""
echo "Alternative: Download manually from:"
echo "  - Pexels: https://www.pexels.com/search/videos/snowstorm/"
echo "  - Pixabay: https://pixabay.com/videos/search/snowstorm/"
echo "  - Coverr: https://coverr.co/"
echo "  - Mixkit: https://mixkit.co/free-stock-video/"
echo ""
echo "Then place the file at: $VIDEO_FILE"
exit 1
