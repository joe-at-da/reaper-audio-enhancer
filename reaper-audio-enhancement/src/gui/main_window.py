import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTabWidget, QProgressBar, QMessageBox,
    QComboBox, QSlider, QSpinBox, QMenuBar, QMenu
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from src.utils import app_logger, config
from src.audio import NoiseDetector, NoiseReducer, AudioSuggester
from src.video import FrameExtractor, SceneDetector
from src.reaper import ExportGenerator
from src.localization import get_localization
from src.gui.settings_dialog import SettingsDialog

class AnalysisThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, audio_path, video_path, localization=None):
        super().__init__()
        self.audio_path = audio_path
        self.video_path = video_path
        self.localization = localization
    
    def run(self):
        try:
            results = {}
            
            # Get localized messages
            analyzing_audio_msg = self.localization.get("analyzing_audio") if self.localization else "Analyzing audio..."
            detecting_scenes_msg = self.localization.get("detecting_scenes") if self.localization else "Detecting scenes..."
            generating_suggestions_msg = self.localization.get("generating_suggestions") if self.localization else "Generating suggestions..."
            analysis_complete_msg = self.localization.get("analysis_complete") if self.localization else "Analysis complete"
            
            self.progress.emit(analyzing_audio_msg)
            noise_detector = NoiseDetector()
            results["audio_analysis"] = noise_detector.analyze_audio(self.audio_path)
            
            if self.video_path:
                self.progress.emit(detecting_scenes_msg)
                scene_detector = SceneDetector()
                results["scenes"] = scene_detector.detect_scenes(self.video_path)
                results["dominant_scene"] = scene_detector.get_dominant_scene(results["scenes"])
                
                self.progress.emit(generating_suggestions_msg)
                audio_suggester = AudioSuggester()
                detected_scenes = [(s["scene_type"], s["confidence"]) for s in results["scenes"]]
                results["suggestions"] = audio_suggester.suggest_audio_for_scene(detected_scenes)
            
            self.progress.emit(analysis_complete_msg)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self, demo_mode=False):
        super().__init__()
        self.localization = get_localization()
        self.audio_file = None
        self.video_file = None
        self.analysis_results = None
        self.demo_mode = demo_mode
        self.init_ui()
        self.create_menu_bar()
        
        if demo_mode:
            self.load_demo_files()
    
    def init_ui(self):
        self.setWindowTitle(self.localization.get("app_title"))
        self.setGeometry(100, 100, 1200, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        self.title_label = QLabel(self.localization.get("app_subtitle"))
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)
        
        intro_text = (
            self.localization.get("welcome_title") + "\n\n" +
            self.localization.get("welcome_text") + "\n\n" +
            self.localization.get("quick_start_title") + "\n" +
            self.localization.get("quick_start_steps")
        )
        self.intro_label = QLabel(intro_text)
        intro_font = QFont()
        intro_font.setPointSize(10)
        self.intro_label.setFont(intro_font)
        self.intro_label.setStyleSheet("color: #cccccc; background-color: #2a2a2a; padding: 15px; border-radius: 5px;")
        layout.addWidget(self.intro_label)
        
        layout.addWidget(QLabel(""))
        
        file_layout = QHBoxLayout()
        
        self.audio_file_label = QLabel(self.localization.get("audio_file_label"))
        file_layout.addWidget(self.audio_file_label)
        self.audio_label = QLabel(self.localization.get("no_file_selected"))
        file_layout.addWidget(self.audio_label)
        self.audio_btn = QPushButton(self.localization.get("browse_audio_button"))
        self.audio_btn.setToolTip(self.localization.get("tooltip_analyze"))
        self.audio_btn.clicked.connect(self.select_audio)
        file_layout.addWidget(self.audio_btn)
        
        layout.addLayout(file_layout)
        
        video_layout = QHBoxLayout()
        
        self.video_file_label = QLabel(self.localization.get("video_file_label"))
        video_layout.addWidget(self.video_file_label)
        self.video_label = QLabel(self.localization.get("no_file_selected_optional"))
        video_layout.addWidget(self.video_label)
        self.video_btn = QPushButton(self.localization.get("browse_video_button"))
        self.video_btn.setToolTip(self.localization.get("tooltip_analyze"))
        self.video_btn.clicked.connect(self.select_video)
        video_layout.addWidget(self.video_btn)
        
        layout.addLayout(video_layout)
        
        settings_layout = QHBoxLayout()
        
        self.noise_reduction_label = QLabel(self.localization.get("noise_reduction_label"))
        settings_layout.addWidget(self.noise_reduction_label)
        self.strength_slider = QSlider(Qt.Horizontal)
        self.strength_slider.setMinimum(0)
        self.strength_slider.setMaximum(100)
        self.strength_slider.setValue(50)
        self.strength_slider.setToolTip(self.localization.get("tooltip_noise_reduction"))
        settings_layout.addWidget(self.strength_slider)
        self.strength_label = QLabel("0.5")
        settings_layout.addWidget(self.strength_label)
        self.strength_slider.valueChanged.connect(self.update_strength_label)
        
        layout.addLayout(settings_layout)
        
        button_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton(self.localization.get("analyze_button"))
        self.analyze_btn.setToolTip(self.localization.get("tooltip_analyze"))
        self.analyze_btn.clicked.connect(self.analyze)
        button_layout.addWidget(self.analyze_btn)
        
        self.process_btn = QPushButton(self.localization.get("process_audio_button"))
        self.process_btn.setToolTip(self.localization.get("tooltip_process_audio"))
        self.process_btn.clicked.connect(self.process_audio)
        button_layout.addWidget(self.process_btn)
        
        self.export_btn = QPushButton(self.localization.get("export_reaper_button"))
        self.export_btn.setToolTip(self.localization.get("tooltip_export_reaper"))
        self.export_btn.clicked.connect(self.export_to_reaper)
        button_layout.addWidget(self.export_btn)
        
        layout.addLayout(button_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel(self.localization.get("ready_status"))
        status_font = QFont()
        status_font.setPointSize(9)
        status_font.setItalic(True)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #888888;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        central_widget.setLayout(layout)
    
    def load_demo_files(self):
        """Load sample files for demo/onboarding mode."""
        try:
            project_root = Path(__file__).parent.parent.parent
            audio_file = project_root / "assets" / "sample_files" / "sample_audio.wav"
            video_file = project_root / "assets" / "sample_files" / "sample_video.mp4"
            
            if audio_file.exists():
                self.audio_file = str(audio_file)
                self.audio_label.setText(f"{audio_file.name} (Demo)")
                demo_audio_msg = self.localization.get("demo_mode_audio_only")
                self.status_label.setText(demo_audio_msg)
            
            if video_file.exists():
                self.video_file = str(video_file)
                self.video_label.setText(f"{video_file.name} (Demo)")
                demo_loaded_msg = self.localization.get("demo_mode_loaded")
                self.status_label.setText(demo_loaded_msg)
                
            app_logger.info("Demo files loaded successfully")
        except Exception as e:
            app_logger.error(f"Error loading demo files: {e}")
    
    def select_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "",
            "Audio Files (*.wav *.mp3 *.flac);;All Files (*)"
        )
        if file_path:
            self.audio_file = file_path
            self.audio_label.setText(Path(file_path).name)
            self.status_label.setText(f"Audio loaded: {Path(file_path).name}")
    
    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "",
            "Video Files (*.mp4 *.mov *.avi);;All Files (*)"
        )
        if file_path:
            self.video_file = file_path
            self.video_label.setText(Path(file_path).name)
            self.status_label.setText(f"Video loaded: {Path(file_path).name}")
    
    def update_strength_label(self, value):
        strength = value / 100.0
        self.strength_label.setText(f"{strength:.2f}")
        config.set("noise_reduction_strength", strength)
    
    def analyze(self):
        if not self.audio_file:
            error_msg = self.localization.get("error_no_audio_select")
            QMessageBox.warning(self, "Error", error_msg)
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.analysis_thread = AnalysisThread(self.audio_file, self.video_file, self.localization)
        self.analysis_thread.progress.connect(self.update_progress)
        self.analysis_thread.finished.connect(self.on_analysis_finished)
        self.analysis_thread.error.connect(self.on_analysis_error)
        self.analysis_thread.start()
    
    def update_progress(self, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(self.progress_bar.value() + 25)
    
    def on_analysis_finished(self, results):
        self.analysis_results = results
        self.progress_bar.setVisible(False)
        
        scene_info = ""
        if "dominant_scene" in results and results["dominant_scene"]:
            scene = results["dominant_scene"]
            detected_text = self.localization.get("detected")
            confidence_text = self.localization.get("confidence")
            scene_info = f" | {detected_text} {scene['scene_type']} ({scene['confidence']:.0%})"
        
        suggestions_info = ""
        if "suggestions" in results:
            suggestions_text = self.localization.get("suggestions")
            suggestions_info = f" | {len(results['suggestions'])} {suggestions_text}"
        
        analysis_complete_text = self.localization.get("analysis_complete")
        self.status_label.setText(f"{analysis_complete_text}{scene_info}{suggestions_info}")
    
    def on_analysis_error(self, error):
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Analysis Error", f"Error during analysis: {error}")
        app_logger.error(f"Analysis error: {error}")
    
    def process_audio(self):
        if not self.audio_file or not self.analysis_results:
            error_msg = self.localization.get("error_no_audio_analyze")
            QMessageBox.warning(self, "Error", error_msg)
            return
        
        try:
            output_path = Path(self.audio_file).parent / f"processed_{Path(self.audio_file).name}"
            
            strength = config.get("noise_reduction_strength", 0.5)
            reducer = NoiseReducer()
            reducer.apply_noise_reduction(self.audio_file, str(output_path), strength)
            
            success_msg = self.localization.get("audio_processed_success")
            self.status_label.setText(f"{success_msg}: {output_path.name}")
            QMessageBox.information(self, "Success", f"{success_msg}: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing audio: {e}")
            app_logger.error(f"Processing error: {e}")
    
    def export_to_reaper(self):
        if not self.analysis_results:
            error_msg = self.localization.get("error_no_audio_analyze")
            QMessageBox.warning(self, "Error", error_msg)
            return
        
        try:
            export_data = {
                "audio_file": self.audio_file,
                "video_file": self.video_file,
                "noise_reduction_strength": config.get("noise_reduction_strength", 0.5),
                "suggestions": self.analysis_results.get("suggestions", []),
            }
            
            exporter = ExportGenerator()
            export_path = exporter.generate_export(export_data)
            
            export_success_msg = self.localization.get("export_success")
            self.status_label.setText(f"{export_success_msg}: {export_path.name}")
            QMessageBox.information(self, "Success", f"{export_success_msg}: {export_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting: {e}")
            app_logger.error(f"Export error: {e}")
    
    def create_menu_bar(self):
        """Create menu bar with Settings menu and language flags."""
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # Ensure menu bar is visible on macOS
        
        # Settings menu
        settings_menu = menubar.addMenu(self.localization.get("settings_menu"))
        
        # Language submenu with flags
        language_menu = settings_menu.addMenu(self.localization.get("language_menu"))
        
        # Add language options with flags
        lang_flags = {
            "en": "🇺🇸 English",
            "uk": "🇺🇦 Українська"
        }
        
        for lang_code in self.localization.get_supported_languages():
            flag_text = lang_flags.get(lang_code, self.localization.get_language_name(lang_code))
            action = language_menu.addAction(flag_text)
            action.triggered.connect(lambda checked, code=lang_code: self.change_language(code))
        
        # Settings dialog option
        settings_menu.addSeparator()
        settings_action = settings_menu.addAction(self.localization.get("settings_menu"))
        settings_action.triggered.connect(self.open_settings_dialog)
    
    def change_language(self, language_code):
        """Change application language."""
        self.localization.set_language(language_code)
        self.refresh_ui()
    
    def open_settings_dialog(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self)
        dialog.language_changed.connect(self.refresh_ui)
        dialog.exec_()
    
    def refresh_ui(self):
        """Refresh UI with new language strings."""
        try:
            # Update window title
            self.setWindowTitle(self.localization.get("app_title"))
            
            # Update title and intro sections
            self.title_label.setText(self.localization.get("app_subtitle"))
            intro_text = (
                self.localization.get("welcome_title") + "\n\n" +
                self.localization.get("welcome_text") + "\n\n" +
                self.localization.get("quick_start_title") + "\n" +
                self.localization.get("quick_start_steps")
            )
            self.intro_label.setText(intro_text)
            
            # Update all labels
            self.audio_file_label.setText(self.localization.get("audio_file_label"))
            self.video_file_label.setText(self.localization.get("video_file_label"))
            self.noise_reduction_label.setText(self.localization.get("noise_reduction_label"))
            self.status_label.setText(self.localization.get("ready_status"))
            
            # Update all buttons
            self.audio_btn.setText(self.localization.get("browse_audio_button"))
            self.audio_btn.setToolTip(self.localization.get("tooltip_analyze"))
            self.video_btn.setText(self.localization.get("browse_video_button"))
            self.video_btn.setToolTip(self.localization.get("tooltip_analyze"))
            self.analyze_btn.setText(self.localization.get("analyze_button"))
            self.analyze_btn.setToolTip(self.localization.get("tooltip_analyze"))
            self.process_btn.setText(self.localization.get("process_audio_button"))
            self.process_btn.setToolTip(self.localization.get("tooltip_process_audio"))
            self.export_btn.setText(self.localization.get("export_reaper_button"))
            self.export_btn.setToolTip(self.localization.get("tooltip_export_reaper"))
            
            # Update slider tooltip
            self.strength_slider.setToolTip(self.localization.get("tooltip_noise_reduction"))
            
            # Recreate menu bar
            self.menuBar().clear()
            self.create_menu_bar()
            
            app_logger.info(f"UI refreshed with language: {self.localization.get_current_language()}")
        except Exception as e:
            app_logger.error(f"Error refreshing UI: {e}")
