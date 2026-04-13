#!/usr/bin/env python3
"""
Command-line tool to import audio enhancement results into REAPER.

Usage:
    python import_to_reaper.py <json_file> [--method osc|reascript|auto]

Examples:
    python import_to_reaper.py ~/.reaper_audio_enhancement/exports/export_20260413_220423.json
    python import_to_reaper.py export.json --method osc
    python import_to_reaper.py export.json --method reascript
"""

import sys
import argparse
from pathlib import Path

from src.reaper.reaper_importer import ReaperImporter
from src.reaper.osc_importer import OSCImporter
from src.reaper.reascript_importer import ReaScriptImporter
from src.utils import app_logger


def main():
    parser = argparse.ArgumentParser(
        description="Import audio enhancement results into REAPER"
    )
    parser.add_argument(
        "json_file",
        help="Path to the exported JSON file"
    )
    parser.add_argument(
        "--method",
        choices=["osc", "reascript", "auto"],
        default="auto",
        help="Import method: osc (live), reascript (script), or auto (try OSC first)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("REAPER Audio Enhancement Importer")
    print("="*60 + "\n")
    
    # Load and validate JSON
    print(f"Loading JSON file: {args.json_file}")
    importer = ReaperImporter()
    
    if not importer.import_json(args.json_file):
        print("✗ Failed to load JSON file")
        return 1
    
    print("✓ JSON file loaded successfully")
    
    # Validate audio files
    print("\nValidating audio files...")
    validation = importer.validate_audio_files()
    
    if not validation["audio_file"]:
        print("✗ Original audio file not found")
        return 1
    print("✓ Original audio file found")
    
    if validation["video_file"]:
        print("✓ Video file found")
    else:
        print("⚠ Video file not found (optional)")
    
    missing_enhancement = [f for f, exists in validation["enhancement_files"].items() if not exists]
    if missing_enhancement:
        print(f"⚠ {len(missing_enhancement)} enhancement file(s) not found:")
        for f in missing_enhancement:
            print(f"  - {f}")
    else:
        print(f"✓ All {len(validation['enhancement_files'])} enhancement files found")
    
    # Determine import method
    print("\nDetermining import method...")
    if args.method == "auto":
        method = importer.get_import_method()
    else:
        method = args.method
    
    print(f"Using method: {method.upper()}")
    
    # Import based on method
    print("\nImporting into REAPER...")
    export_data = importer.get_export_data()
    
    if method == "osc":
        success = import_via_osc(export_data)
    else:
        success = import_via_reascript(export_data)
    
    if success:
        print("\n" + "="*60)
        print("✓ Import successful!")
        print("="*60)
        print("\nYour REAPER project now contains:")
        print(f"  • Original Audio track")
        if export_data.get("video_track", {}).get("file"):
            print(f"  • Video track")
        print(f"  • {len(export_data.get('enhancement_tracks', []))} Enhancement track(s)")
        print("\n")
        return 0
    else:
        print("\n" + "="*60)
        print("✗ Import failed")
        print("="*60 + "\n")
        return 1


def import_via_osc(export_data):
    """
    Import using OSC (Open Sound Control).
    """
    try:
        print("  Connecting to REAPER via OSC...")
        osc = OSCImporter()
        
        if not osc.connect():
            print("  ✗ Could not connect to REAPER")
            print("    Make sure REAPER is running and OSC is enabled")
            print("    (REAPER > Options > Preferences > Control/OSC/web)")
            return False
        
        print("  ✓ Connected to REAPER")
        
        print("  Creating tracks...")
        if not osc.import_from_data(export_data):
            print("  ✗ Failed to create tracks")
            return False
        
        print("  ✓ Tracks created successfully")
        osc.disconnect()
        return True
    except Exception as e:
        app_logger.error(f"OSC import error: {e}")
        print(f"  ✗ OSC import failed: {e}")
        return False


def import_via_reascript(export_data):
    """
    Import using ReaScript.
    """
    try:
        print("  Generating ReaScript...")
        reascript = ReaScriptImporter()
        script_path = reascript.save_reascript(export_data)
        
        if not script_path:
            print("  ✗ Failed to generate ReaScript")
            return False
        
        print("  ✓ ReaScript generated")
        print(f"\n  Script saved to: {script_path}")
        print("\n  To import into REAPER:")
        print("    1. Open REAPER")
        print("    2. Go to: Actions > Show Console")
        print("    3. Click 'Load' and select the script file")
        print("    4. Click 'Run'")
        print("\n  Or run directly in REAPER's Python console")
        
        return True
    except Exception as e:
        app_logger.error(f"ReaScript generation error: {e}")
        print(f"  ✗ ReaScript generation failed: {e}")
        return False


if __name__ == "__main__":
    sys.exit(main())
