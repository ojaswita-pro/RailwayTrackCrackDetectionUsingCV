"""
Captured_images.py
------------------
Continuously captures frames from the webcam and saves them
to the 'captured_images' directory with timestamped filenames.
Used as the live image feed source for railway crack detection.
"""

import cv2
import os
import time
from datetime import datetime

# === Configuration ===
SAVE_DIR = 'captured_images'  # Folder to store captured images
CAPTURE_INTERVAL = 1          # Time between captures (in seconds)

# Ensure directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[×] Error: Could not open webcam.")
    exit()

print("[+] Webcam initialized. Starting image capture...")
print(f"[*] Saving images to: {os.path.abspath(SAVE_DIR)}")

# === Main Loop ===
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[-] Warning: Failed to grab frame. Retrying...")
            time.sleep(0.5)
            continue

        # Generate timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(SAVE_DIR, f"image_{timestamp}.jpg")

        # Save captured frame
        cv2.imwrite(filename, frame)
        print(f"[✓] Saved: {filename}")

        # Wait for next capture
        time.sleep(CAPTURE_INTERVAL)

except KeyboardInterrupt:
    print("\n[!] Image capture stopped by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("[✓] Camera released and resources cleaned up.")
