import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow
from src.utils import app_logger

def main():
    demo_mode = "--demo" in sys.argv or "-d" in sys.argv
    
    if demo_mode:
        app_logger.info("Starting REAPER Audio Enhancement Tool (DEMO MODE)")
    else:
        app_logger.info("Starting REAPER Audio Enhancement Tool")
    
    app = QApplication(sys.argv)
    window = MainWindow(demo_mode=demo_mode)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
