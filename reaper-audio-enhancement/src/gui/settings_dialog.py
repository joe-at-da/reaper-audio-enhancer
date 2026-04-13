from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton, QGroupBox, QLineEdit, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from src.localization import get_localization
from src.utils import config


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
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton(self.localization.get("english"))  # Reuse for cancel
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.reject)
        
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
    
    def save_settings(self):
        """Save settings to config."""
        # Save REAPER OSC settings
        osc_host = self.osc_host_input.text().strip() or "127.0.0.1"
        osc_port = self.osc_port_input.value()
        
        config.set("osc_host", osc_host)
        config.set("osc_port", osc_port)
    
    def accept(self):
        """Accept and save settings."""
        self.save_settings()
        super().accept()
    
    def on_language_changed(self):
        """Handle language change."""
        lang_code = self.language_combo.currentData()
        if lang_code:
            self.localization.set_language(lang_code)
            self.language_changed.emit(lang_code)
    
    def get_selected_language(self):
        """Get the selected language code."""
        return self.language_combo.currentData()
