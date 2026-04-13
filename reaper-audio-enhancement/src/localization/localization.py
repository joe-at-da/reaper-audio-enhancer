import json
from pathlib import Path
from src.utils import config, app_logger


class Localization:
    """Manages application localization and language switching."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Localization, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.strings = {}
        self.current_language = "en"
        self.supported_languages = ["en", "uk"]
        
        self._load_strings()
        self._load_language_preference()
    
    def _load_strings(self):
        """Load translation strings from JSON file."""
        try:
            strings_file = Path(__file__).parent / "strings.json"
            with open(strings_file, 'r', encoding='utf-8') as f:
                self.strings = json.load(f)
            app_logger.info(f"Loaded translations for languages: {list(self.strings.keys())}")
        except Exception as e:
            app_logger.error(f"Error loading strings: {e}")
            self.strings = {"en": {}, "uk": {}}
    
    def _load_language_preference(self):
        """Load saved language preference from config."""
        try:
            saved_lang = config.get("language")
            if saved_lang and saved_lang in self.supported_languages:
                self.current_language = saved_lang
                app_logger.info(f"Loaded language preference: {saved_lang}")
            else:
                # Try to detect system language
                system_lang = self._detect_system_language()
                self.current_language = system_lang
                config.set("language", system_lang)
                app_logger.info(f"Detected system language: {system_lang}")
        except Exception as e:
            app_logger.error(f"Error loading language preference: {e}")
            self.current_language = "en"
    
    def _detect_system_language(self):
        """Detect system language and return supported language code."""
        try:
            import locale
            import os
            
            # Try multiple methods to detect system language
            system_locale = None
            
            # Method 1: locale.getdefaultlocale()
            try:
                system_locale = locale.getdefaultlocale()[0]
            except:
                pass
            
            # Method 2: LANG environment variable (macOS/Linux)
            if not system_locale:
                system_locale = os.environ.get('LANG', '')
            
            # Method 3: LC_ALL environment variable
            if not system_locale:
                system_locale = os.environ.get('LC_ALL', '')
            
            if system_locale:
                lang_code = system_locale.split('_')[0].lower()
                
                # Map common locale codes to supported languages
                if lang_code == "uk":
                    app_logger.info(f"Detected Ukrainian from locale: {system_locale}")
                    return "uk"
                elif lang_code in ["en"]:
                    app_logger.info(f"Detected English from locale: {system_locale}")
                    return "en"
            
            app_logger.info(f"Could not detect language from locale, defaulting to English")
            return "en"  # Default to English
        except Exception as e:
            app_logger.error(f"Error detecting system language: {e}")
            return "en"
    
    def get(self, key, default=""):
        """Get translated string for current language."""
        try:
            if self.current_language in self.strings:
                return self.strings[self.current_language].get(key, default)
            return default
        except Exception as e:
            app_logger.error(f"Error getting string '{key}': {e}")
            return default
    
    def set_language(self, language_code):
        """Change the current language."""
        if language_code in self.supported_languages:
            self.current_language = language_code
            config.set("language", language_code)
            app_logger.info(f"Language changed to: {language_code}")
            return True
        else:
            app_logger.warning(f"Unsupported language: {language_code}")
            return False
    
    def get_current_language(self):
        """Get the current language code."""
        return self.current_language
    
    def get_supported_languages(self):
        """Get list of supported language codes."""
        return self.supported_languages
    
    def get_language_name(self, language_code):
        """Get display name for a language code."""
        names = {
            "en": "English",
            "uk": "Українська"
        }
        return names.get(language_code, language_code)


# Singleton instance
_localization = Localization()


def get_localization():
    """Get the localization singleton instance."""
    return _localization


def _(key, default=""):
    """Shorthand for getting translated strings."""
    return _localization.get(key, default)
