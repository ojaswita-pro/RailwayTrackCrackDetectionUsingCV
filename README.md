🚄 Railway Crack Detection System

This project detects cracks on railway tracks using a custom-trained YOLOv8 model.
It automates image capture, real-time detection, and alert generation to improve railway safety.

🧠 Project Overview

YOLOv8 is used for crack detection.

OpenCV captures real-time images using a connected camera.

Flask provides a simple web interface to visualize detection results.

Twilio (optional) can send SMS alerts with GPS location when a crack is detected.

🗂 Folder Structure

RailwayCrackWeb/
│
├── app.py # Flask web server
├── launcher.py # Launches camera, detection, and web modules
├── detect_and_save.py # Runs YOLOv8 detection on captured images
├── Captured_images.py # Captures images using OpenCV
│
├── model/ # Folder for YOLOv8 model
│ └── best.pt # (Add your trained model here)
│
├── static/
│ └── images/ # Stores output images with detections
│
├── templates/
│ └── index.html # Web interface
│
├── detection_log.json # Log of detection results
├── requirements.txt # Python dependencies (optional)
└── README.md # Project documentation

⚙️ Setup Instructions
1️⃣ Clone the Repository

git clone https://github.com/
<your-username>/RailwayCrackWeb.git
cd RailwayCrackWeb

2️⃣ Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate # For Linux/Mac
venv\Scripts\activate # For Windows

3️⃣ Install Dependencies

pip install ultralytics opencv-python flask certifi twilio

🏋️‍♀️ Model Training

If you don’t have best.pt, train your own YOLOv8 model using:
yolo detect train data=dataset/data.yaml model=yolov8n.pt epochs=50 imgsz=640

After training, place the best.pt file inside the model/ directory.

🚀 Running the System
Method 1: Launch All Components Automatically

python launcher.py

This starts:

Image capture (Captured_images.py)

YOLO detection (detect_and_save.py)

Flask web app (app.py)

Method 2: Run Individually (Optional)

python Captured_images.py
python detect_and_save.py
python app.py

🌐 Viewing Results

After launching, open your browser and go to:
http://127.0.0.1:5000/

You’ll see the latest detection results and images.
