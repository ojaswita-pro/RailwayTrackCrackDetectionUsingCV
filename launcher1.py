"""
Railway Crack Detection System Launcher
---------------------------------------
Safely launches all project components:
1. Captured_images.py  – handles camera input
2. detect_and_save.py  – performs YOLOv8 detection
3. app.py              – runs Flask web interface
Modules are started only if their dependencies are installed.
"""

import subprocess
import sys
import time
from importlib.util import find_spec

# --- Helper: check if module is installed ---
def is_module_available(module_name: str) -> bool:
    """Return True if the specified Python module is installed."""
    return find_spec(module_name) is not None

# --- Helper: start a Python script safely ---
def start_script(script_name: str, module_needed: str = None):
    """
    Starts a subprocess for the given Python script.
    If 'module_needed' is provided and not found, the script is skipped.
    """
    if module_needed and not is_module_available(module_needed):
        print(f"[!] Skipping {script_name} — required module '{module_needed}' not found.")
        print(f"    ➜ Install it with: pip install {module_needed}\n")
        return None

    try:
        process = subprocess.Popen([sys.executable, script_name])
        print(f"[+] Started {script_name}")
        return process
    except Exception as e:
        print(f"[!] Failed to start {script_name}: {e}")
        return None


# === Launch Sequence ===
print("\n🚆 === Railway Crack Detection System Launcher ===\n")

# Step 1️⃣: Start camera capture
camera_proc = start_script("Captured_images.py", module_needed="cv2")

# Step 2️⃣: Small delay for stability
time.sleep(1)

# Step 3️⃣: Start YOLOv8 detection
detection_proc = start_script("detect_and_save.py", module_needed="certifi")

# Step 4️⃣: Small delay again
time.sleep(1)

# Step 5️⃣: Start Flask web server
web_proc = start_script("app.py", module_needed="flask")

print("\n[✓] All available components started successfully (missing ones skipped).")
print("[ℹ] Press Ctrl + C to stop all running processes.\n")

# === Process Monitor ===
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[!] KeyboardInterrupt received — stopping all processes...")
    for proc in [camera_proc, detection_proc, web_proc]:
        if proc:
            proc.terminate()
    print("[✓] All processes safely terminated.")
