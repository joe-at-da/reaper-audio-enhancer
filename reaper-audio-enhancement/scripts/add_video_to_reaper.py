#!/usr/bin/env python3
"""
REAPER ReaScript to add video file to current project.
This script should be run from within REAPER as a Python ReaScript.

Usage:
1. In REAPER: Actions > Show action list
2. New... > Create new action
3. Paste this script
4. Run it

Or copy to REAPER's Scripts folder:
  macOS: ~/Library/Application Support/REAPER/Scripts/
  Windows: %APPDATA%\REAPER\Scripts\
  Linux: ~/.config/REAPER/Scripts/
"""

import os
import sys

# This will be available when running as a ReaScript in REAPER
try:
    import reaper
except ImportError:
    print("ERROR: This script must be run from within REAPER as a ReaScript")
    sys.exit(1)

def add_video_to_reaper(video_path):
    """Add video file to current REAPER project."""
    
    # Check if file exists
    if not os.path.exists(video_path):
        reaper.ShowMessageBox(f"Video file not found:\n{video_path}", "Error", 0)
        return False
    
    try:
        # Get the current project
        project = 0  # 0 = current project
        
        # Create or get the video track
        # First, count existing tracks
        track_count = reaper.CountTracks(project)
        
        # Create a new track for video
        reaper.InsertTrackAtIndex(track_count, True)
        video_track = reaper.GetTrack(project, track_count)
        
        # Set track name
        reaper.GetSetMediaTrackInfo_String(video_track, "P_NAME", "Video", True)
        
        # Create a media item on the video track
        item = reaper.AddMediaItemToTrack(video_track)
        
        if not item:
            reaper.ShowMessageBox("Failed to create media item", "Error", 0)
            return False
        
        # Create a source from the video file
        source = reaper.PCM_Source_CreateFromFile(video_path)
        
        if not source:
            reaper.ShowMessageBox(f"Failed to load video file:\n{video_path}", "Error", 0)
            return False
        
        # Get the active take of the item
        take = reaper.GetActiveTake(item)
        
        if not take:
            reaper.ShowMessageBox("Failed to create take", "Error", 0)
            return False
        
        # Set the source for the take
        reaper.SetMediaItemTake_Source(take, source)
        
        # Get video duration
        source_length = reaper.GetMediaSourceLength(source)
        
        # Set item length to match video duration
        reaper.SetMediaItemLength(item, source_length, False)
        
        # Refresh REAPER UI
        reaper.UpdateArrange()
        
        reaper.ShowMessageBox(
            f"Video added successfully!\n\n"
            f"File: {os.path.basename(video_path)}\n"
            f"Duration: {source_length:.2f}s\n\n"
            f"To view video:\n"
            f"1. View > Video Window (Cmd+Shift+V)\n"
            f"2. Click Play",
            "Success",
            0
        )
        
        return True
        
    except Exception as e:
        reaper.ShowMessageBox(f"Error adding video:\n{str(e)}", "Error", 0)
        return False

def main():
    """Main entry point."""
    
    # Get video file path from user
    # Try to find sample video first
    sample_video = os.path.expanduser(
        "~/Projects/ihor-audio-main/reaper-audio-enhancement/assets/sample_files/sample_video.mp4"
    )
    
    # If sample doesn't exist, ask user to browse
    if not os.path.exists(sample_video):
        # Open file browser
        retval, video_path = reaper.GetUserFileNameForRead(
            "",
            "Select Video File",
            "*.mp4;*.mov;*.avi;*.webm"
        )
        
        if retval == 0 or not video_path:
            return
        
        sample_video = video_path
    
    # Add the video
    add_video_to_reaper(sample_video)

if __name__ == "__main__":
    main()
