#!/usr/bin/env python3
"""
Simple launcher script - run from project root directory
Usage: 
  python run.py              # Normal mode
  python run.py --demo       # Demo mode with sample files pre-loaded
  python run.py -d           # Short form of demo mode
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import main

if __name__ == "__main__":
    main()
