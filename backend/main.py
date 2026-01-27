from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from food_detection.yolo_detector import detect_food_items
from gl_calculation import calculate_glycemic_load


# --------------------------------------------------
# App Initialization
# --------------------------------------------------
app = FastAPI(
    title="AI Glycemic Load & Glucose Prediction API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Food name normalization mapping
# (YOLO output → Nutrition DB labels)
# --------------------------------------------------
FOOD_NAME_MAPPING = {
    "rice": "white_rice",
    "idli": "idli",
    "dosa": "dosa",
    "sambar": "sambar",
    "dal": "dal"
}


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# --------------------------------------------------
# Analyze Meal Endpoint
# --------------------------------------------------
@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    """
    End-to-end pipeline:
    Image → YOLO food detection → normalization → deduplication
    → GL calculation → glucose prediction → recommendation
    """

    # ---------------------------------------------- 
    # 1. Read image bytes
    # ----------------------------------------------
    image_bytes = await file.read()

    # ----------------------------------------------
    # 2. Detect food items using YOLOv8
    # ----------------------------------------------
    detected_foods = detect_food_items(image_bytes)

    # Safety fallback (if YOLO fails)
    if not detected_foods:
     return {
        "foods": [],
        "glycemic_load": 0,
        "predicted_glucose": None,
        "recommendation": "No food detected. Please upload a clearer image."
    }


    # ----------------------------------------------
    # 3. Normalize food names
    # (IMPORTANT FIX #1)
    # ----------------------------------------------
    normalized_foods = []
    for food in detected_foods:
        mapped_name = FOOD_NAME_MAPPING.get(food["name"], food["name"])
        normalized_foods.append({
            "name": mapped_name,
            "confidence": food["confidence"]
        })

    # ----------------------------------------------
    # 4. Remove duplicate food detections
    # (IMPORTANT FIX #2 — DUPLICATION LOGIC IS HERE)
    # ----------------------------------------------
    unique_foods = {}
    for food in normalized_foods:
        name = food["name"]
        confidence = food["confidence"]

        # Keep highest confidence instance only
        if name not in unique_foods or confidence > unique_foods[name]["confidence"]:
            unique_foods[name] = food

    final_foods = list(unique_foods.values())

    # ----------------------------------------------
    # 5. Glycemic Load Calculation
    # ----------------------------------------------
    PORTION_GRAMS = 200  # assumed portion (research prototype)
    total_gl = 0.0

    for food in final_foods:
        gl_value = calculate_glycemic_load(
            food_name=food["name"],
            portion_grams=PORTION_GRAMS
        )
        if gl_value is not None:
            total_gl += gl_value

    total_gl = round(total_gl, 2)

    # ----------------------------------------------
    # 6. Temporary Glucose Prediction
    # (Will be replaced by LSTM in Step 5)
    # ----------------------------------------------
    predicted_glucose = 180 + int(total_gl * 0.3)

    # ----------------------------------------------
    # 7. Rule-based Recommendation
    # ----------------------------------------------
    if predicted_glucose >= 180:
        recommendation = "Walk for 15–20 minutes to reduce glucose spike"
    elif predicted_glucose < 70:
        recommendation = "Consume a small carbohydrate snack"
    else:
        recommendation = "Glucose level expected to remain stable"

    # ----------------------------------------------
    # 8. Final Response
    # ----------------------------------------------
    response = {
        "foods": final_foods,
        "glycemic_load": total_gl,
        "predicted_glucose": predicted_glucose,
        "recommendation": recommendation
    }

    return response
