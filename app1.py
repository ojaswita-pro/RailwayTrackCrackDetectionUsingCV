"""
Railway Crack Detection Web Server
----------------------------------
Serves the web dashboard for real-time crack detection results.
Displays the latest detection image and location details
fetched from detection_log.json.
"""

from flask import Flask, render_template, jsonify, send_from_directory
import json
import os

# === Flask App Initialization ===
app = Flask(__name__, static_folder='static', template_folder='templates')

# === Configuration Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "detection_log.json")
IMAGE_DIR = os.path.join(BASE_DIR, "static", "images")

# === Routes ===
@app.route('/')
def index():
    """Render the main web interface."""
    return render_template('index.html')

@app.route('/api/latest-detection')
def latest_detection():
    """
    Return the most recent detection entry from detection_log.json.
    If no log file or entry exists, return an empty JSON object.
    """
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    return jsonify(data[-1])
        except json.JSONDecodeError:
            print("[!] Warning: detection_log.json is corrupted or empty.")
    return jsonify({})

@app.route('/images/<filename>')
def serve_image(filename):
    """Serve detection images from the static/images folder."""
    return send_from_directory(IMAGE_DIR, filename)

# === Entry Point ===
if __name__ == '__main__':
    # Run in production-friendly mode (no debug info exposed)
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
