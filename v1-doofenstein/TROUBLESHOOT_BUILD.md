# Troubleshooting the Windows Build

The `build_windows.bat` script may have failed silently. Here's how to fix it.

---

## **Quick Fix: Use Python Build Script**

Instead of the batch file, use the Python script (works on Windows, Mac, Linux):

```bash
# Open Command Prompt or PowerShell
cd C:\path\to\GLUTCHDEXMALL

# Run the build script
python build.py
```

This will:
1. Install PyInstaller (if needed)
2. Clean old builds
3. Build the executable
4. Show you the result (or detailed error if it fails)

**This is the most reliable method.**

---

## **If Python Script Fails**

### **Error: "Python is not recognized"**

**Solution:** Python isn't in your PATH. Try:

```bash
# Use full path to Python
C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe build.py
```

Or reinstall Python from https://www.python.org and **CHECK "Add Python to PATH"** during installation.

### **Error: "PyInstaller not found"**

**Solution:** Install it manually:

```bash
pip install pyinstaller
```

Then run:
```bash
pyinstaller glitchdex_mall.spec
```

### **Error: Permission denied**

**Solution:** Run Command Prompt as Administrator:
1. Right-click Command Prompt
2. Select "Run as administrator"
3. Run the build script again

---

## **Manual Build (No Batch File)**

If automated scripts aren't working, build manually:

### **Step 1: Install PyInstaller**
```bash
pip install pyinstaller
```

### **Step 2: Clean old builds**
```bash
rmdir /s /q build
rmdir /s /q dist
```

### **Step 3: Build**
```bash
pyinstaller glitchdex_mall.spec
```

### **Step 4: Check result**
```bash
dir dist\glitchdex-mall\
```

You should see:
```
glitchdex-mall.exe
_internal/
data/
```

---

## **Verify the Build**

Once build completes, check that files exist:

```bash
# Navigate to build output
cd dist\glitchdex-mall\

# List contents
dir

# Run the game
glitchdex-mall.exe
```

---

## **Common Issues**

### **Issue: EXE crashes on startup (quick flash)**

**Cause:** Data files not found

**Solution:**
1. Check that `data/` folder exists in `dist/glitchdex-mall/data/`
2. Check that `_internal/` folder exists
3. Rebuild: `pyinstaller glitchdex_mall.spec`

### **Issue: "ModuleNotFoundError"**

**Cause:** Hidden import missing

**Solution:** Check that `src/main.py` exists and is valid:
```bash
python src/main.py
```

If Python version works but EXE doesn't, PyInstaller is missing a module.

Edit `glitchdex_mall.spec` and add:
```python
hiddenimports=['game_loop', 'mall_engine', 'entities', 'renderer', 'toddler_system'],
```

Then rebuild.

### **Issue: Data files not in EXE**

**Cause:** `glitchdex_mall.spec` not configured correctly

**Solution:** Check that `datas=` section exists:
```python
datas=[
    ('data', 'data'),
    ('docs', 'docs'),
    ('examples', 'examples'),
],
```

---

## **Testing the EXE**

Once built, test it:

```bash
# From dist\glitchdex-mall\ folder
glitchdex-mall.exe

# Should see:
# 1. Welcome screen
# 2. Game menu or gameplay
# 3. Can play normally
```

If it works, you can:
1. Double-click it from Explorer to run
2. Share the entire `dist\glitchdex-mall\` folder
3. Create a ZIP of that folder for distribution

---

## **Packaging for Distribution**

Once EXE works, create a distribution ZIP:

```bash
# From GLUTCHDEXMALL folder
cd dist\

# Create ZIP
# (Use Windows Explorer: right-click glitchdex-mall → Send To → Compressed folder)
# Or use PowerShell:
Compress-Archive -Path glitchdex-mall -DestinationPath glitchdex-mall-v1.0.zip

# Result: glitchdex-mall-v1.0.zip (ready to share!)
```

---

## **Alternative: Launcher EXE Wrapper**

If the game EXE isn't working but Python is, use the launcher instead:

```bash
# Build launcher EXE instead
pyinstaller --onefile src/launcher.py

# This creates: dist\launcher.exe
# Which launches the 1990s shareware menu
```

---

## **Getting Detailed Error Messages**

If EXE closes silently, get error details:

### **Option 1: Run from Command Prompt**
```bash
cd dist\glitchdex-mall\
glitchdex-mall.exe 2>&1 | tee output.txt

# Shows errors in output.txt
```

### **Option 2: Use debugpy (for advanced debugging)**
```bash
pip install debugpy
python -m debugpy.adapter glitchdex-mall.exe
```

### **Option 3: Check Windows Event Viewer**
1. Right-click Start Menu
2. Event Viewer
3. Windows Logs → System
4. Look for crashes from `glitchdex-mall.exe`

---

## **Success Checklist**

✓ `dist/` folder exists
✓ `dist/glitchdex-mall/` folder exists
✓ `glitchdex-mall.exe` exists
✓ `_internal/` folder exists with Python runtime
✓ `data/` folder exists with JSON files
✓ EXE runs (doesn't flash and close)
✓ Game menu appears
✓ Can navigate and play

---

## **Still Stuck?**

1. **Try Python version first:**
   ```bash
   python src/main.py
   ```

   If this works, the problem is PyInstaller bundling, not the game.

2. **Check Python version:**
   ```bash
   python --version
   ```

   Must be 3.8+

3. **Rebuild clean:**
   ```bash
   rmdir /s /q build dist
   python build.py
   ```

4. **Check file permissions:**
   - Right-click EXE
   - Properties
   - Check "Unblock" checkbox at bottom
   - Apply

---

## **Quick Commands Reference**

```bash
# Install PyInstaller
pip install pyinstaller

# Build with Python script (recommended)
python build.py

# Manual build
pyinstaller glitchdex_mall.spec

# Test if Python version works
python src/main.py

# Navigate to built exe
cd dist\glitchdex-mall\

# Run the exe
glitchdex-mall.exe

# Clean for rebuild
rmdir /s /q build dist
```

---

**If you get an error message from running `python build.py`, paste it here and I can fix the spec file immediately.**
