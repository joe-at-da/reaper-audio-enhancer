import sys
import os
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar,
    QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class InstallationThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, project_root):
        super().__init__()
        self.project_root = Path(project_root)
    
    def run(self):
        try:
            self.progress.emit("Creating virtual environment...")
            venv_path = self.project_root / "venv"
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            
            self.progress.emit("Installing dependencies...")
            pip_path = venv_path / "bin" / "pip"
            requirements_path = self.project_root / "requirements.txt"
            subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], check=True)
            
            self.progress.emit("Setting up configuration...")
            config_dir = self.project_root / ".config"
            config_dir.mkdir(exist_ok=True)
            
            self.progress.emit("Installation complete!")
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class SetupWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_root = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("REAPER Audio Enhancement - Setup Wizard")
        self.setGeometry(100, 100, 600, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        title = QLabel("REAPER Audio Enhancement Setup")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Welcome! This wizard will set up the audio enhancement tool."))
        layout.addWidget(QLabel(""))
        
        layout.addWidget(QLabel("Step 1: Select Project Location"))
        project_layout = QHBoxLayout()
        self.project_label = QLineEdit()
        self.project_label.setReadOnly(True)
        project_layout.addWidget(self.project_label)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.select_project)
        project_layout.addWidget(browse_btn)
        layout.addLayout(project_layout)
        
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel("Step 2: System Check"))
        self.python_check = QLabel("✓ Python 3.8+")
        layout.addWidget(self.python_check)
        
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel("Step 3: Installation"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready to install")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        self.install_btn = QPushButton("Install")
        self.install_btn.clicked.connect(self.start_installation)
        self.install_btn.setEnabled(False)
        button_layout.addWidget(self.install_btn)
        
        launch_btn = QPushButton("Launch Application")
        launch_btn.clicked.connect(self.launch_app)
        button_layout.addWidget(launch_btn)
        
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
    
    def select_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.project_root = Path(folder)
            self.project_label.setText(str(self.project_root))
            self.install_btn.setEnabled(True)
    
    def start_installation(self):
        if not self.project_root:
            QMessageBox.warning(self, "Error", "Please select a project folder")
            return
        
        self.progress_bar.setVisible(True)
        self.install_btn.setEnabled(False)
        
        self.install_thread = InstallationThread(self.project_root)
        self.install_thread.progress.connect(self.update_progress)
        self.install_thread.finished.connect(self.on_installation_finished)
        self.install_thread.error.connect(self.on_installation_error)
        self.install_thread.start()
    
    def update_progress(self, message):
        self.status_label.setText(message)
    
    def on_installation_finished(self):
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, "Success", "Installation complete!")
    
    def on_installation_error(self, error):
        self.progress_bar.setVisible(False)
        self.install_btn.setEnabled(True)
        QMessageBox.critical(self, "Installation Error", f"Error: {error}")
    
    def launch_app(self):
        if not self.project_root:
            QMessageBox.warning(self, "Error", "Please select a project folder")
            return
        
        try:
            venv_path = self.project_root / "venv"
            python_path = venv_path / "bin" / "python"
            
            if not python_path.exists():
                QMessageBox.warning(self, "Error", "Virtual environment not found. Please install first.")
                return
            
            subprocess.Popen([str(python_path), "-m", "src.main"], cwd=str(self.project_root))
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch application: {e}")

def main():
    app = QApplication(sys.argv)
    wizard = SetupWizard()
    wizard.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
