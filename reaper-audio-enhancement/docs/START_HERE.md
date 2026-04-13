# START HERE - How to Run the Application

## ⚠️ Important: You Must Be in the Correct Directory

The application is located in:
```
/Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement/
```

**You MUST navigate to this directory before running the application.**

---

## Quick Start (Copy & Paste)

### Step 1: Navigate to the Project Directory
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
```

### Step 2: Run the Application

**Option A: Using the Launch Script (Easiest)**
```bash
bash launch.sh
```

**Option B: Using Python**
```bash
source venv/bin/activate
python run.py
```

---

## Detailed Instructions

### If You're in the Wrong Directory

**Wrong** ❌
```bash
(venv) (base) ➜  ihor-audio-main source venv/bin/activate
```
This won't work because `venv` is not in `ihor-audio-main/`

**Correct** ✓
```bash
(venv) (base) ➜  ihor-audio-main cd reaper-audio-enhancement
(venv) (base) ➜  reaper-audio-enhancement source venv/bin/activate
```

### Full Step-by-Step

1. **Open Terminal**

2. **Navigate to the Project**
   ```bash
   cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
   ```
   
   You should see:
   ```
   ➜  reaper-audio-enhancement
   ```

3. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```
   
   You should see:
   ```
   (venv) ➜  reaper-audio-enhancement
   ```

4. **Run the Application**
   ```bash
   python run.py
   ```
   
   Or use the launcher:
   ```bash
   bash launch.sh
   ```

5. **Application Should Launch**
   - A window titled "REAPER Audio Enhancement Tool" will appear
   - You'll see the introduction and quick start instructions
   - Ready to use!

---

## Troubleshooting

### Error: "No such file or directory"
**Cause**: You're in the wrong directory

**Solution**: 
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
```

### Error: "ModuleNotFoundError: No module named 'src'"
**Cause**: You're in the wrong directory or didn't activate venv

**Solution**:
1. Make sure you're in: `/Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement`
2. Activate venv: `source venv/bin/activate`
3. Run: `python run.py`

### Error: "venv: command not found"
**Cause**: Virtual environment doesn't exist

**Solution**: Create it first
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

---

## Directory Structure

```
/Users/joebradley/Projects/
└── ihor-audio-main/
    └── reaper-audio-enhancement/          ← YOU ARE HERE
        ├── venv/                          ← Virtual environment
        ├── src/                           ← Source code
        ├── assets/                        ← Sample files
        ├── run.py                         ← Launcher script
        ├── launch.sh                      ← Shell launcher
        ├── requirements.txt               ← Dependencies
        └── ... (other files)
```

---

## What Each Launch Method Does

### Method 1: `bash launch.sh` (Easiest)
- Automatically activates venv
- Runs the application
- No manual steps needed

### Method 2: `python run.py`
- Requires manual venv activation first
- More control
- Good for development

### Method 3: `python src/main.py`
- Direct execution
- Requires proper path setup
- Not recommended for regular use

---

## Verify Everything Works

### Check Virtual Environment
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
source venv/bin/activate
which python
```

Should show path to venv python, like:
```
/Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement/venv/bin/python
```

### Check Imports
```bash
python -c "from src.gui import MainWindow; print('✓ OK')"
```

Should output:
```
✓ OK
```

### Run Tests
```bash
python -m pytest tests/ -v
```

Should show all tests passing.

---

## Common Mistakes

### ❌ Mistake 1: Running from Wrong Directory
```bash
cd /Users/joebradley/Projects/ihor-audio-main
source venv/bin/activate  # This will fail - venv is not here!
```

### ✓ Correct
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
source venv/bin/activate  # This works - venv is here!
```

### ❌ Mistake 2: Not Activating Virtual Environment
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
python run.py  # May use system Python instead of venv
```

### ✓ Correct
```bash
cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement
source venv/bin/activate
python run.py
```

### ❌ Mistake 3: Using Conda Instead of venv
```bash
conda activate base  # This is for conda, not this project
```

### ✓ Correct
```bash
source venv/bin/activate  # This is for this project's venv
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Navigate to project | `cd /Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement` |
| Activate venv | `source venv/bin/activate` |
| Run app (easy) | `bash launch.sh` |
| Run app (manual) | `python run.py` |
| Run tests | `python -m pytest tests/ -v` |
| Check imports | `python -c "from src.gui import MainWindow; print('✓ OK')"` |
| Deactivate venv | `deactivate` |

---

## Still Having Issues?

1. **Verify directory**: `pwd` should show `/Users/joebradley/Projects/ihor-audio-main/reaper-audio-enhancement`
2. **Check venv**: `ls venv/` should show `bin/`, `lib/`, etc.
3. **Check Python**: `which python` should show path to venv
4. **Check imports**: `python -c "from src.gui import MainWindow; print('OK')"`
5. **Run tests**: `python -m pytest tests/ -v`

If you still have issues, provide the exact error message and the output of `pwd`.

---

## Next Steps

Once the application is running:
1. See `USER_GUIDE.md` for how to use it
2. Try the sample files in `assets/sample_files/`
3. Read `QUICKSTART.md` for workflow examples

---

**Remember: Always be in the `reaper-audio-enhancement` directory before running!**
