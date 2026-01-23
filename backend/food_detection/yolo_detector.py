from ultralytics import YOLO
from PIL import Image
import tempfile
import os

# Load YOLOv8 model once
model = YOLO("yolov8n.pt")

# Temporary mapping (extend later)
FOOD_CLASSES = {
    "bowl": "rice",
    "pizza": "pizza",
    "sandwich": "sandwich"
}

def detect_food_items(image_bytes):
    """
    Detect food items from image using YOLOv8.
    Returns list of detected food names with confidence.
    """

    # Create temp file (Windows-safe)
    temp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    try:
        temp.write(image_bytes)
        temp.close()

        image = Image.open(temp.name)
        results = model(image)

        detected_foods = []

        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])

                if class_name in FOOD_CLASSES:
                    detected_foods.append({
                        "name": FOOD_CLASSES[class_name],
                        "confidence": round(confidence, 2)
                    })

        return detected_foods

    finally:
        # Always delete temp file
        if os.path.exists(temp.name):
            os.remove(temp.name)
