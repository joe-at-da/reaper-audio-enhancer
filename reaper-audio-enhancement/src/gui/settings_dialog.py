import sys
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton, QGroupBox, QLineEdit, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from src.localization import get_localization
from src.utils import config
from src.utils.vlc_detector import get_vlc_detector


class SettingsDialog(QDialog):
    """Settings dialog for application preferences."""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.localization = get_localization()
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle(self.localization.get("settings_menu"))
        self.setGeometry(100, 100, 500, 350)
        
        layout = QVBoxLayout()
        
        # Language settings group
        language_group = QGroupBox(self.localization.get("language_menu"))
        language_layout = QHBoxLayout()
        
        language_label = QLabel(self.localization.get("language_menu") + ":")
        self.language_combo = QComboBox()
        
        # Add supported languages
        for lang_code in self.localization.get_supported_languages():
            lang_name = self.localization.get_language_name(lang_code)
            self.language_combo.addItem(lang_name, lang_code)
        
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        language_group.setLayout(language_layout)
        
        layout.addWidget(language_group)
        
        # REAPER settings group
        reaper_group = QGroupBox("REAPER OSC Settings")
        reaper_layout = QVBoxLayout()
        
        # OSC Host
        host_layout = QHBoxLayout()
        host_label = QLabel("OSC Host:")
        self.osc_host_input = QLineEdit()
        self.osc_host_input.setPlaceholderText("127.0.0.1")
        host_layout.addWidget(host_label)
        host_layout.addWidget(self.osc_host_input)
        reaper_layout.addLayout(host_layout)
        
        # OSC Port
        port_layout = QHBoxLayout()
        port_label = QLabel("OSC Port:")
        self.osc_port_input = QSpinBox()
        self.osc_port_input.setMinimum(1)
        self.osc_port_input.setMaximum(65535)
        self.osc_port_input.setValue(9000)
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.osc_port_input)
        port_layout.addStretch()
        reaper_layout.addLayout(port_layout)
        
        # Info label
        info_label = QLabel("Configure REAPER OSC connection settings.\nDefault: 127.0.0.1:9000")
        info_label.setStyleSheet("color: #888888; font-size: 9pt;")
        reaper_layout.addWidget(info_label)
        
        reaper_group.setLayout(reaper_layout)
        layout.addWidget(reaper_group)
        
        # VLC settings group
        vlc_group = QGroupBox(self.localization.get("vlc_title"))
        vlc_layout = QVBoxLayout()
        
        # VLC status
        vlc_detector = get_vlc_detector()
        vlc_status_label = QLabel(self.localization.get("vlc_status") + ":")
        
        if vlc_detector.is_installed():
            vlc_status_text = self.localization.get("vlc_installed")
            vlc_path = vlc_detector.get_vlc_path()
            vlc_status_value = QLabel(f"{vlc_status_text} ✓")
            vlc_status_value.setStyleSheet("color: #51cf66;")
        else:
            vlc_status_text = self.localization.get("vlc_not_installed")
            vlc_status_value = QLabel(vlc_status_text)
            vlc_status_value.setStyleSheet("color: #ff6b6b;")
        
        vlc_status_layout = QHBoxLayout()
        vlc_status_layout.addWidget(vlc_status_label)
        vlc_status_layout.addWidget(vlc_status_value)
        vlc_status_layout.addStretch()
        vlc_layout.addLayout(vlc_status_layout)
        
        # VLC path input
        vlc_path_layout = QHBoxLayout()
        vlc_path_label = QLabel("VLC Path:")
        self.vlc_path_input = QLineEdit()
        self.vlc_path_input.setPlaceholderText(vlc_detector.get_vlc_path() or "Not found")
        vlc_path_layout.addWidget(vlc_path_label)
        vlc_path_layout.addWidget(self.vlc_path_input)
        vlc_layout.addLayout(vlc_path_layout)
        
        # VLC download button (if not installed)
        if not vlc_detector.is_installed():
            vlc_button_layout = QHBoxLayout()
            vlc_download_button = QPushButton(self.localization.get("vlc_download_link"))
            vlc_download_button.clicked.connect(self.open_vlc_download)
            vlc_button_layout.addWidget(vlc_download_button)
            vlc_button_layout.addStretch()
            vlc_layout.addLayout(vlc_button_layout)
        
        # VLC info
        vlc_info_label = QLabel(self.localization.get("vlc_instructions"))
        vlc_info_label.setStyleSheet("color: #888888; font-size: 9pt;")
        vlc_info_label.setWordWrap(True)
        vlc_layout.addWidget(vlc_info_label)
        
        vlc_group.setLayout(vlc_layout)
        layout.addWidget(vlc_group)
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        help_button = QPushButton("📖 Getting Started")
        help_button.clicked.connect(self.open_getting_started)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton(self.localization.get("english"))  # Reuse for cancel
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(help_button)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """Load current settings into dialog."""
        current_lang = self.localization.get_current_language()
        index = self.language_combo.findData(current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        
        # Load REAPER OSC settings
        osc_host = config.get("osc_host", "127.0.0.1")
        osc_port = config.get("osc_port", 9000)
        
        self.osc_host_input.setText(osc_host)
        self.osc_port_input.setValue(osc_port)
        
        # Load VLC path
        vlc_detector = get_vlc_detector()
        vlc_path = config.get("vlc_path", vlc_detector.get_vlc_path() or "")
        self.vlc_path_input.setText(vlc_path)
    
    def save_settings(self):
        """Save settings to config."""
        # Save REAPER OSC settings
        osc_host = self.osc_host_input.text().strip() or "127.0.0.1"
        osc_port = self.osc_port_input.value()
        
        config.set("osc_host", osc_host)
        config.set("osc_port", osc_port)
        
        # Save VLC path
        vlc_path = self.vlc_path_input.text().strip()
        if vlc_path:
            config.set("vlc_path", vlc_path)
    
    def accept(self):
        """Accept and save settings."""
        self.save_settings()
        super().accept()
    
    def on_language_changed(self):
        """Handle language change."""
        lang_code = self.language_combo.currentData()
        if lang_code:
            self.localization.set_language(lang_code)
            self.refresh_ui()
            self.language_changed.emit(lang_code)
    
    def refresh_ui(self):
        """Refresh UI with new language."""
        try:
            # Update window title
            self.setWindowTitle(self.localization.get("settings_menu"))
            
            # Update group box titles
            # Language group is already updated via combo box
            
            # Update REAPER group info
            reaper_info = self.findChild(type(self), "reaper_info")
            if reaper_info:
                reaper_info.setText("Configure REAPER OSC connection settings.\nDefault: 127.0.0.1:9000")
            
            # Update VLC group title and info
            vlc_info_label = self.findChild(type(self), "vlc_info")
            if vlc_info_label:
                vlc_info_label.setText(self.localization.get("vlc_instructions"))
        except Exception as e:
            from src.utils import app_logger
            app_logger.error(f"Error refreshing Settings UI: {e}")
    
    def get_selected_language(self):
        """Get the selected language code."""
        return self.language_combo.currentData()
    
    def open_vlc_download(self):
        """Open VLC download page in browser."""
        vlc_detector = get_vlc_detector()
        url = vlc_detector.get_installation_url()
        QDesktopServices.openUrl(QUrl(url))
    
    def open_getting_started(self):
        """Open Getting Started guide in default text editor."""
        from pathlib import Path
        import subprocess
        
        # Get current language and select appropriate guide
        current_lang = self.localization.get_current_language()
        
        if current_lang == "uk":
            guide_file = "GETTING_STARTED_UK.md"
        else:
            guide_file = "GETTING_STARTED.md"
        
        docs_path = Path(__file__).parent.parent.parent / "docs" / guide_file
        
        if docs_path.exists():
            try:
                # Open with default application
                if sys.platform == "darwin":  # macOS
                    subprocess.Popen(["open", str(docs_path)])
                elif sys.platform == "win32":  # Windows
                    subprocess.Popen(["notepad", str(docs_path)])
                else:  # Linux
                    subprocess.Popen(["xdg-open", str(docs_path)])
            except Exception as e:
                from src.utils import app_logger
                app_logger.error(f"Error opening Getting Started guide: {e}")
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "File Not Found", 
                              f"Getting Started guide not found at:\n{docs_path}")
