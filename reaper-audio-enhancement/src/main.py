import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow
from src.utils import app_logger

def main():
    demo_mode = False
    demo_type = None
    
    # Parse demo mode arguments
    if "--demo" in sys.argv:
        demo_mode = True
        demo_idx = sys.argv.index("--demo")
        if demo_idx + 1 < len(sys.argv):
            demo_type = sys.argv[demo_idx + 1]
    elif "-d" in sys.argv:
        demo_mode = True
        demo_idx = sys.argv.index("-d")
        if demo_idx + 1 < len(sys.argv):
            demo_type = sys.argv[demo_idx + 1]
    
    if demo_mode:
        demo_label = f" ({demo_type})" if demo_type else ""
        app_logger.info(f"Starting REAPER Audio Enhancement Tool (DEMO MODE{demo_label})")
    else:
        app_logger.info("Starting REAPER Audio Enhancement Tool")
    
    app = QApplication(sys.argv)
    window = MainWindow(demo_mode=demo_mode, demo_type=demo_type)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
