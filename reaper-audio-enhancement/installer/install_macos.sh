#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=========================================="
echo "REAPER Audio Enhancement - macOS Installer"
echo "=========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"
echo ""

echo "Creating virtual environment..."
python3 -m venv "$PROJECT_ROOT/venv"
source "$PROJECT_ROOT/venv/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r "$PROJECT_ROOT/requirements.txt"

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "To launch the application:"
echo "  cd $PROJECT_ROOT"
echo "  source venv/bin/activate"
echo "  python src/main.py"
echo ""
echo "Or run the setup wizard:"
echo "  python installer/setup_wizard.py"
echo ""
