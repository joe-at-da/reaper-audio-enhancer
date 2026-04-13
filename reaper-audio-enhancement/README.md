# REAPER Audio Enhancement Plugin

A hybrid Python tool with GUI for removing noise and suggesting contextual audio enhancements based on video content.

## Features

- **Noise Detection & Reduction**: Identify and reduce background noise using spectral subtraction
- **Scene Detection**: Analyze video to detect context (storm, car ride, indoor, etc.)
- **Audio Suggestions**: Recommend and apply contextual ambient sounds
- **REAPER Integration**: Export processing instructions for seamless REAPER workflow
- **Separate Tracks**: Maintains separate audio and video tracks for flexibility

## Quick Start

### Installation

#### macOS
```bash
bash installer/install_macos.sh
```

#### Windows
```cmd
installer\install_windows.bat
```

### Manual Setup
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python src/main.py
```

## Usage

1. Launch the application
2. Load an audio/video file
3. Run analysis to detect noise and scenes
4. Review suggestions
5. Accept/reject changes
6. Export to REAPER or save processed audio

## Project Structure

```
reaper-audio-enhancement/
├── src/
│   ├── gui/              # PyQt5 GUI components
│   ├── audio/            # Audio processing modules
│   ├── video/            # Video analysis modules
│   ├── reaper/           # REAPER integration
│   └── utils/            # Utilities and config
├── installer/            # Setup wizards for macOS/Windows
├── assets/               # Audio library and samples
└── tests/                # Unit tests
```

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run application
python src/main.py
```

## Requirements

- Python 3.8+
- macOS 10.14+ or Windows 10+
- REAPER (for full integration)
- 2GB RAM minimum

## License

MIT
