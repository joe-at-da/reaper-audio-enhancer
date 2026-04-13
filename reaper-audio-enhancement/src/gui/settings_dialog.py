from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QPushButton, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from src.localization import get_localization


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
        self.setGeometry(100, 100, 400, 200)
        
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
    
    def on_language_changed(self):
        """Handle language change."""
        lang_code = self.language_combo.currentData()
        if lang_code:
            self.localization.set_language(lang_code)
            self.language_changed.emit(lang_code)
    
    def get_selected_language(self):
        """Get the selected language code."""
        return self.language_combo.currentData()
