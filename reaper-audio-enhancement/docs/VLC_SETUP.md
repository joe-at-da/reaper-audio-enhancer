# VLC Setup for Video Playback in REAPER

**Required for**: Video display in REAPER arrange window

---

## Overview

REAPER uses VLC (VideoLAN) for video playback. Without VLC installed and configured, REAPER can import video files but won't display them in the arrange window.

---

## Installation by System

### macOS

**Option 1: Download from VideoLAN**
1. Visit: https://www.videolan.org/vlc/download-macos.html
2. Download VLC for macOS
3. Open the `.dmg` file
4. Drag VLC to Applications folder
5. Restart REAPER

**Option 2: Homebrew**
```bash
brew install vlc
```

**Verification**
```bash
ls /Applications/VLC.app
# or
which vlc
```

### Windows

**Option 1: Download from VideoLAN**
1. Visit: https://www.videolan.org/vlc/download-windows.html
2. Download VLC installer
3. Run the installer
4. Follow the installation wizard
5. Restart REAPER

**Option 2: Chocolatey**
```bash
choco install vlc
```

**Verification**
```cmd
where vlc
# or check Program Files
dir "C:\Program Files\VideoLAN\VLC"
```

### Linux

**Ubuntu/Debian**
```bash
sudo apt-get update
sudo apt-get install vlc
```

**Fedora/RHEL**
```bash
sudo dnf install vlc
```

**Arch**
```bash
sudo pacman -S vlc
```

**Verification**
```bash
which vlc
# or
vlc --version
```

---

## REAPER Configuration

### Auto-Detection (Recommended)

REAPER will automatically detect VLC if:
1. VLC is installed in standard location
2. VLC is in system PATH
3. REAPER is restarted after VLC installation

### Manual Configuration

If REAPER doesn't auto-detect VLC:

1. **Open REAPER Preferences**
   - REAPER > Preferences (macOS)
   - Options > Preferences (Windows/Linux)

2. **Find Video Settings**
   - Search for "Video" in preferences
   - Look for "Video Playback" or "Video Processor"

3. **Set VLC Path**
   - macOS: `/Applications/VLC.app/Contents/MacOS/VLC`
   - Windows: `C:\Program Files\VideoLAN\VLC\vlc.exe`
   - Linux: `/usr/bin/vlc`

4. **Apply and Restart REAPER**

---

## Testing Video Playback

### Step 1: Open a Project with Video
1. Launch REAPER
2. Open a project with a video file
3. Or import a video file: Insert > Media File

### Step 2: Open Video Window
- macOS: Cmd+Shift+V
- Windows/Linux: Ctrl+Shift+V
- Or: View > Video Window

### Step 3: Play
1. Click Play button
2. Video should display in Video Window
3. Audio plays simultaneously

### Troubleshooting

**Video window opens but shows black screen**
- VLC might not be configured correctly
- Try restarting REAPER
- Check REAPER preferences for VLC path

**Video window doesn't open**
- VLC might not be installed
- Check installation (see above)
- Verify REAPER can find VLC

**Video plays but is choppy/slow**
- This is normal for complex video
- Try reducing video resolution
- Close other applications
- Check system resources

---

## Our Tool's VLC Detection

The REAPER Audio Enhancement Tool includes automatic VLC detection:

```python
from src.utils.vlc_detector import get_vlc_detector

detector = get_vlc_detector()

# Check if VLC is installed
if detector.is_installed():
    print(f"VLC found at: {detector.get_vlc_path()}")
else:
    print("VLC not found")
    # Get installation instructions
    instructions = detector.get_installation_instructions()
    print(instructions)
```

**Features**:
- ✓ Auto-detects VLC on macOS, Windows, Linux
- ✓ Checks multiple common locations
- ✓ Provides installation instructions
- ✓ Integrated into Settings dialog

---

## Settings Integration

The application Settings dialog shows:

**VLC Status**
- Installed / Not Installed
- VLC path (if found)
- Installation instructions (if not found)
- Link to download VLC

**VLC Setup Button**
- Opens VLC download page
- Provides system-specific instructions
- Guides through installation

---

## Why VLC is Required

REAPER uses VLC because:
1. **Cross-platform**: Works on macOS, Windows, Linux
2. **Reliable**: Handles most video formats
3. **Efficient**: Optimized for video playback
4. **Free**: Open source, no licensing issues

---

## Supported Video Formats

With VLC, REAPER supports:
- MP4 (H.264, H.265)
- MOV (QuickTime)
- AVI
- WebM
- MKV
- FLV
- WMV
- And many more

---

## Performance Tips

1. **Use H.264 codec** for best compatibility
2. **720p or 1080p** resolution is ideal
3. **Close other applications** for smooth playback
4. **Update VLC** regularly for best performance
5. **Use SSD** for video files (faster access)

---

## Troubleshooting Checklist

- [ ] VLC is installed
- [ ] VLC is in standard location or PATH
- [ ] REAPER has been restarted after VLC installation
- [ ] Video file is in supported format (MP4, MOV, AVI)
- [ ] Video file is not corrupted
- [ ] REAPER preferences show VLC path
- [ ] Video Window is open (Cmd/Ctrl+Shift+V)
- [ ] System has enough resources (RAM, CPU)

---

## Getting Help

If you have issues:

1. **Check VLC installation**
   ```bash
   # macOS/Linux
   which vlc
   vlc --version
   
   # Windows
   where vlc
   ```

2. **Check REAPER preferences**
   - Verify VLC path is correct
   - Try auto-detect again

3. **Test VLC directly**
   ```bash
   vlc /path/to/video.mp4
   ```

4. **Check REAPER logs**
   - REAPER > Help > Show REAPER resource path
   - Check reaper-errors.txt

---

## Summary

✓ VLC is required for video playback  
✓ Installation is simple (download and install)  
✓ REAPER auto-detects VLC  
✓ Our tool helps with VLC detection  
✓ Video playback works once VLC is configured  

**Video display in REAPER requires VLC. Installation takes 2-3 minutes.**
