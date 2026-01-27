from ultralytics import YOLO
from PIL import Image
import tempfile
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "runs/detect/train/weights/best.pt"

model = YOLO(str(MODEL_PATH))

def detect_food_items(image_bytes):
    temp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)

    try:
        temp.write(image_bytes)
        temp.close()

        image = Image.open(temp.name)
        results = model(image, conf=0.15)

        detected_foods = []

        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                print("RAW YOLO PREDICTION:", class_name)

                confidence = float(box.conf[0])

                detected_foods.append({
                    "name": class_name,
                    "confidence": round(confidence, 2)
                })

        return detected_foods

    finally:
        if os.path.exists(temp.name):
            os.remove(temp.name)
