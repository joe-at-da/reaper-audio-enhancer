# Localization Setup & Configuration

## Overview

The REAPER Audio Enhancement Tool now supports multiple languages with automatic system language detection and easy switching between English and Ukrainian.

---

## Features Implemented

### 1. Multi-Language Support
- ✓ English (en)
- ✓ Ukrainian (Українська - uk)
- ✓ Easy to add more languages

### 2. System Language Detection
- ✓ Auto-detects system language on startup
- ✓ Works on macOS and Windows
- ✓ Falls back to English if unsupported

### 3. Language Switching
- ✓ Settings menu with language options
- ✓ Settings dialog for preferences
- ✓ Language preference persisted across sessions
- ✓ Real-time UI refresh when language changes

### 4. Comprehensive Translation
- ✓ All UI labels translated
- ✓ All buttons translated
- ✓ All tooltips translated
- ✓ All status messages translated
- ✓ 40+ strings translated to Ukrainian

---

## How to Use

### Automatic Language Detection

When you launch the application:
1. System language is detected automatically
2. If system is set to Ukrainian → App launches in Ukrainian
3. If system is set to English → App launches in English
4. If system language is unsupported → Defaults to English

### Changing Language via Settings Menu

1. Click **Settings** in the menu bar
2. Select **Language** submenu
3. Choose your preferred language:
   - English
   - Українська (Ukrainian)
4. UI updates immediately

### Changing Language via Settings Dialog

1. Click **Settings** in the menu bar
2. Select **Settings** option
3. Choose language from dropdown
4. Click **OK**
5. UI updates immediately

---

## Technical Implementation

### File Structure

```
src/localization/
├── __init__.py              # Package initialization
├── strings.json             # All UI text (EN & UK)
└── localization.py          # Localization manager
```

### strings.json Format

```json
{
  "en": {
    "app_title": "REAPER Audio Enhancement Tool",
    "audio_file_label": "Audio File:",
    ...
  },
  "uk": {
    "app_title": "Інструмент покращення аудіо REAPER",
    "audio_file_label": "Аудіо файл:",
    ...
  }
}
```

### Localization Manager

The `Localization` class provides:
- `get(key)` - Get translated string
- `set_language(code)` - Change language
- `get_current_language()` - Get current language
- `get_supported_languages()` - List available languages
- `_detect_system_language()` - Auto-detect system language

### GUI Integration

All UI elements use localization:
```python
from src.localization import get_localization

localization = get_localization()
button_text = localization.get("analyze_button")  # Returns translated text
```

---

## Translated Strings

### English (40+ strings)
- Application title and subtitle
- Welcome message and quick start
- All button labels
- All field labels
- All tooltips
- Status messages
- Error messages

### Ukrainian (40+ strings)
- Інструмент покращення аудіо REAPER
- Аналізувати
- Обробити аудіо
- Експортувати в REAPER
- And 36+ more...

---

## Configuration

### Language Preference Storage

Language preference is saved to:
```
~/.reaper_audio_enhancement/config.json
```

**Example**:
```json
{
  "language": "uk",
  "osc_host": "127.0.0.1",
  "osc_port": 9000,
  ...
}
```

### System Language Detection

Supported system locales:
- `en_*` → English
- `uk_*` → Ukrainian
- Others → Default to English

**Examples**:
- macOS: `en_US` → English
- macOS: `uk_UA` → Ukrainian
- Windows: `English_United States` → English
- Windows: `Ukrainian_Ukraine` → Ukrainian

---

## Adding New Languages

To add a new language (e.g., Spanish):

### Step 1: Update strings.json

```json
{
  "en": { ... },
  "uk": { ... },
  "es": {
    "app_title": "Herramienta de mejora de audio REAPER",
    "audio_file_label": "Archivo de audio:",
    ...
  }
}
```

### Step 2: Update localization.py

```python
self.supported_languages = ["en", "uk", "es"]

def get_language_name(self, language_code):
    names = {
        "en": "English",
        "uk": "Українська",
        "es": "Español"
    }
    return names.get(language_code, language_code)
```

### Step 3: Update System Detection (Optional)

```python
def _detect_system_language(self):
    ...
    if lang_code == "es":
        return "es"
    ...
```

---

## Testing Localization

### Test 1: System Language Detection

```bash
# Check detected language
python -c "from src.localization import get_localization; loc = get_localization(); print(loc.get_current_language())"
```

### Test 2: Language Switching

```bash
python -c "
from src.localization import get_localization
loc = get_localization()
print('EN:', loc.get('app_title'))
loc.set_language('uk')
print('UK:', loc.get('app_title'))
"
```

### Test 3: GUI Language Switching

1. Launch app: `bash launch.sh demo`
2. Click Settings → Language
3. Select Ukrainian
4. Verify all text updates
5. Click Settings → Language
6. Select English
7. Verify all text updates back

### Test 4: Persistence

1. Launch app
2. Change to Ukrainian
3. Close app
4. Relaunch app
5. Verify it opens in Ukrainian

---

## Supported Languages

| Language | Code | Status | Strings |
|----------|------|--------|---------|
| English | en | ✓ Complete | 40+ |
| Ukrainian | uk | ✓ Complete | 40+ |
| Spanish | es | ⏳ Future | - |
| German | de | ⏳ Future | - |
| French | fr | ⏳ Future | - |

---

## Best Practices

### For Developers

1. **Always use localization** for user-facing text
   ```python
   # ✓ Good
   label = QLabel(self.localization.get("audio_file_label"))
   
   # ✗ Bad
   label = QLabel("Audio File:")
   ```

2. **Add new strings to strings.json** before using them
   ```json
   "my_new_string": "My new text"
   ```

3. **Test with both languages** before committing
   ```bash
   python run.py --demo
   # Test in English, then switch to Ukrainian
   ```

### For Translators

1. **Maintain consistency** across translations
2. **Keep string length reasonable** (UI layout dependent)
3. **Test in actual UI** to verify appearance
4. **Use proper Ukrainian characters** (Ї, Є, І, Ґ)

---

## Troubleshooting

### Issue: Language Not Changing

**Solution**:
1. Restart the application
2. Check that language code is supported
3. Verify strings.json is valid JSON
4. Check config file permissions

### Issue: Text Not Translating

**Solution**:
1. Verify string key exists in strings.json
2. Check for typos in key name
3. Ensure localization is initialized
4. Check language is set correctly

### Issue: System Language Not Detected

**Solution**:
1. Check system locale settings
2. Verify locale format (e.g., en_US)
3. Check language code mapping
4. Manually set language in Settings

### Issue: Config File Not Saving

**Solution**:
1. Check directory permissions
2. Verify ~/.reaper_audio_enhancement exists
3. Check disk space
4. Try manual language change

---

## Performance

### Localization Impact
- **Minimal**: Strings loaded once at startup
- **Memory**: ~50KB for all translations
- **Speed**: <1ms per string lookup
- **No impact** on audio processing

### Optimization
- Singleton pattern for localization
- Lazy loading of strings
- Efficient dictionary lookups
- No file I/O after initialization

---

## Future Enhancements

### Planned Features
- [ ] More language support (Spanish, German, French)
- [ ] Language selection on first launch
- [ ] Automatic translation updates
- [ ] Community translation platform
- [ ] Right-to-left language support (Arabic, Hebrew)

### Potential Improvements
- [ ] Pluralization support
- [ ] Date/time localization
- [ ] Number formatting
- [ ] Currency support
- [ ] Regional variants (en_GB, en_AU)

---

## Summary

The localization system provides:
- ✓ Automatic system language detection
- ✓ Easy language switching
- ✓ Persistent language preference
- ✓ Comprehensive English & Ukrainian translations
- ✓ Easy to extend with new languages
- ✓ Works on macOS and Windows
- ✓ Minimal performance impact

**Current Status**: ✓ Complete and tested

**Next Steps**:
1. Test with actual users
2. Gather feedback on translations
3. Add more languages based on demand
4. Improve UI refresh on language change

---

**For questions or improvements, refer to the localization code in `src/localization/`.**
