import os
import time
import json
import certifi
import requests
from ultralytics import YOLO
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()  # Reads from .env file

# === CONFIGURATION ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_DIR = os.path.join(BASE_DIR, 'images')
STATIC_DIR = os.path.join(BASE_DIR, 'static/images')
LOG_FILE = os.path.join(BASE_DIR, 'detection_log.json')
MODEL_PATH = os.path.join(BASE_DIR, 'model/best.pt')

# Twilio configuration (safely stored in environment)
TWILIO_ENABLED = os.getenv("TWILIO_ENABLED", "0")  # "1" to enable SMS, "0" to disable
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TARGET_PHONE_NUMBER = os.getenv("TARGET_PHONE_NUMBER")

# === INITIALIZATION ===
model = YOLO(MODEL_PATH)
os.makedirs(STATIC_DIR, exist_ok=True)
processed_images = set()
crack_count = 0  # Track total cracks

print("[+] Detection engine initialized.")
print(f"[*] Watching folder: {CAPTURE_DIR}")

# === FUNCTIONS ===
def get_phone_location():
    """Fetch approximate location using SSL-safe connection."""
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5, verify=certifi.where())
        if response.status_code == 200:
            data = response.json()
            loc = data.get('loc', '0,0')
            latitude, longitude = loc.split(',')
            return latitude, longitude
        else:
            print("[-] Error fetching IP location:", response.status_code)
    except Exception as e:
        print("[-] Location error:", str(e))
    return "0", "0"  # Fallback for offline testing

def send_sms_alert(image_name, latitude, longitude):
    """Send SMS alert only if Twilio is enabled."""
    if TWILIO_ENABLED != "1":
        print("[SMS] Twilio disabled. Skipping alert.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_body = (
            f"⚠️ Crack detected!\n"
            f"File: {image_name}\n"
            f"Location: https://www.google.com/maps?q={latitude},{longitude}"
        )
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=TARGET_PHONE_NUMBER
        )
        print(f"[SMS] Alert sent: SID {message.sid}")
    except Exception as e:
        print(f"[SMS] Failed to send: {e}")

# === MAIN LOOP ===
try:
    while True:
        if not os.path.exists(CAPTURE_DIR):
            print(f"[×] Capture directory '{CAPTURE_DIR}' does not exist. Retrying...")
            time.sleep(1)
            continue

        images = sorted(os.listdir(CAPTURE_DIR))[-5:]  # Check last few images

        if not images:
            print("[×] No images found. Waiting...")
            time.sleep(1)
            continue

        for image in images:
            image_path = os.path.join(CAPTURE_DIR, image)

            if image in processed_images:
                continue

            print(f"[>] Processing: {image_path}")
            results = model(image_path)
            boxes = results[0].boxes

            latitude, longitude = get_phone_location()

            log = {
                "timestamp": time.time(),
                "image": image,
                "latitude": latitude,
                "longitude": longitude
            }

            if boxes is not None and len(boxes) > 0:
                print(f"[✓] Crack(s) detected in: {image_path}")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_name = f"detected_{timestamp}.jpg"
                output_path = os.path.join(STATIC_DIR, output_name)
                results[0].save(filename=output_path)

                num_cracks = len(boxes)
                crack_count += num_cracks

                log["image"] = output_name
                log["message"] = f"{num_cracks} Crack(s) detected!"

                # Update detection log
                try:
                    with open(LOG_FILE, 'r') as f:
                        logs = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    logs = []

                logs.append(log)
                with open(LOG_FILE, 'w') as f:
                    json.dump(logs, f, indent=4)

                print(f"[+] Detection log updated: {LOG_FILE}")
                send_sms_alert(output_name, latitude, longitude)
            else:
                print(f"[×] No crack detected in: {image_path}")

            processed_images.add(image)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[!] KeyboardInterrupt received. Saving final log...")

finally:
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    summary = {
        "timestamp": time.time(),
        "summary": f"Total cracks detected in session: {crack_count}"
    }
    logs.append(summary)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

    print(f"[✓] Final crack count ({crack_count}) saved to log.")
