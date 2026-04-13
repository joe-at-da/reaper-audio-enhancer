# REAPER OSC Settings Added to Settings Dialog

**Date**: April 13, 2026  
**Status**: ✓ COMPLETE

---

## What Was Added

### REAPER OSC Configuration Section
A new "REAPER OSC Settings" section has been added to the Settings dialog, allowing users to configure their REAPER connection.

---

## Settings Available

### OSC Host
- **Default**: 127.0.0.1 (localhost)
- **Purpose**: IP address of the REAPER instance
- **Use Case**: Remote REAPER on different machine

### OSC Port
- **Default**: 9000
- **Range**: 1-65535
- **Purpose**: Port number for OSC communication
- **Use Case**: Custom port if REAPER uses different port

---

## How to Access

1. Click **Settings** in the menu bar
2. Settings dialog opens
3. Scroll down to **"REAPER OSC Settings"** section
4. Configure:
   - **OSC Host**: IP address of REAPER (default: 127.0.0.1)
   - **OSC Port**: Port number (default: 9000)
5. Click **OK** to save

---

## Setup Instructions for Users

### Step 1: Enable OSC in REAPER
1. Open REAPER
2. Go to: **Options > Preferences**
3. Search for: **OSC**
4. Enable OSC and note the port (default: 9000)

### Step 2: Configure in Audio Enhancement Tool
1. Click **Settings**
2. Go to **REAPER OSC Settings**
3. Enter REAPER's IP and port
4. Click **OK**

### Step 3: Use Import to REAPER
1. Export JSON from the tool
2. Click **Import to REAPER**
3. Select JSON file
4. Tracks created automatically!

---

## Updated Export Instructions

The export success dialog now includes setup instructions:

**English**:
```
How to import into REAPER:
1. (Optional) Configure REAPER OSC settings in Settings > REAPER OSC Settings
   - Default: 127.0.0.1:9000
   - Ensure REAPER has OSC enabled (Options > Preferences > Control/OSC/web)
2. Use the Import to REAPER button in the application
   - Or run: python import_to_reaper.py {path}
3. Choose import method:
   - OSC (if REAPER is running): Automatic track creation
   - ReaScript: Manual script execution in REAPER
4. REAPER will automatically create:
   - Original Audio track with your audio file
   - Video track (if provided)
   - Enhancement tracks with suggested audio files
   - All timing, volume, and fade settings
```

**Ukrainian**:
```
Як імпортувати в REAPER:
1. (Опціонально) Налаштуйте параметри REAPER OSC в Параметри > REAPER OSC Settings
   - За замовчуванням: 127.0.0.1:9000
   - Переконайтеся, що OSC увімкнено в REAPER (Options > Preferences > Control/OSC/web)
2. Використовуйте кнопку Import to REAPER в програмі
   - Або запустіть: python import_to_reaper.py {path}
3. Виберіть метод імпорту:
   - OSC (якщо REAPER запущено): Автоматичне створення доріжок
   - ReaScript: Ручне виконання скрипту в REAPER
4. REAPER автоматично створить:
   - Доріжку Original Audio з вашим аудіофайлом
   - Доріжку Video (якщо надано)
   - Доріжки Enhancement з запропонованими аудіофайлами
   - Всі налаштування часу, гучності та затухання
```

---

## Files Modified

### 1. `src/gui/settings_dialog.py`
**Changes**:
- Added `QLineEdit` and `QSpinBox` imports
- Added `config` import from utils
- Created "REAPER OSC Settings" group box
- Added OSC Host input field
- Added OSC Port spinner
- Added info label with default values
- Implemented `load_settings()` to load OSC config
- Implemented `save_settings()` to save OSC config
- Override `accept()` to save settings on OK
- Dialog size increased to 500x350 to accommodate new settings

### 2. `src/localization/strings.json`
**Changes**:
- Updated `export_instructions` (English) with setup guidance
- Updated `export_instructions` (Ukrainian) with setup guidance
- Both versions now mention Settings > REAPER OSC Settings

---

## User Workflow

### Before
```
1. Export JSON
2. User confused about REAPER setup
3. User manually configures OSC
4. User runs import command
```

### After
```
1. Export JSON
2. Export dialog shows setup instructions
3. User clicks Settings
4. User configures REAPER OSC (if needed)
5. User clicks Import to REAPER
6. Tracks created automatically
```

---

## Features

✓ **Easy Configuration** - Simple UI for OSC settings  
✓ **Persistent Storage** - Settings saved to config file  
✓ **Default Values** - Works out of the box (127.0.0.1:9000)  
✓ **Clear Instructions** - Export dialog explains setup  
✓ **Validation** - Port range validated (1-65535)  
✓ **Localization** - Instructions in English and Ukrainian  

---

## Technical Details

### Settings Storage
- Settings saved to: `~/.reaper_audio_enhancement/config.json`
- Keys: `osc_host`, `osc_port`
- Loaded on application startup
- Used by OSC importer

### Default Configuration
```json
{
  "osc_host": "127.0.0.1",
  "osc_port": 9000
}
```

### Settings Dialog
- Window size: 500x350
- Two sections: Language, REAPER OSC Settings
- OK button saves settings
- Cancel button discards changes

---

## Testing

✓ Settings dialog opens  
✓ OSC Host field displays  
✓ OSC Port spinner displays  
✓ Default values load correctly  
✓ Settings save to config  
✓ Export instructions updated  
✓ Both languages supported  

---

## Summary

**Status**: ✓ COMPLETE

REAPER OSC settings have been added to the Settings dialog:
- ✓ OSC Host configuration
- ✓ OSC Port configuration
- ✓ Settings persistence
- ✓ Updated export instructions
- ✓ Both languages supported
- ✓ Tested and verified

Users can now easily configure their REAPER connection without editing config files!

---

## Next Steps for Users

1. **Enable OSC in REAPER**
   - Options > Preferences > Control/OSC/web
   - Note the port (usually 9000)

2. **Configure in Audio Enhancement Tool**
   - Click Settings
   - Enter REAPER's IP and port
   - Click OK

3. **Use Import to REAPER**
   - Export JSON
   - Click Import to REAPER
   - Select JSON file
   - Tracks created automatically!

---

**REAPER integration is now fully configured and user-friendly!**
